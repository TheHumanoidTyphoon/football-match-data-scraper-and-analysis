import argparse
import pandas as pd
from rich import print
from rich.console import Console
import matplotlib.pyplot as plt


def parse_arguments():
    """
    Parses command-line arguments.

    Returns
    -------
    args : argparse.Namespace
        The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Perform data analysis on football match data.")
    parser.add_argument("-i", "--input_file", type=str,
                        default="input_matches_file.csv", help="Path to input CSV file")
    parser.add_argument("-o", "--output_file", type=str,
                        default="output_matches_file.csv", help="Path to output CSV file")
    parser.add_argument("-p", "--plot_type", type=str, default="all", choices=[
                        "all", "percentage", "total_goals"], help="Type of plot to display")
    parser.add_argument("-s", "--show_plot",
                        action="store_true", help="Show plot only")
    return parser.parse_args()


def load_data(file_path):
    """
    Loads data from a CSV file.

    Parameters
    ----------
    file_path : str
        The path to the input CSV file.

    Returns
    -------
    pandas.DataFrame
        The loaded data.
    """
    return pd.read_csv(file_path)


def replace_question_marks_with_zero(df, col_name):
    """
    Replaces all question marks in a column of a DataFrame with 0.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    col_name : str
        The name of the column to replace question marks.

    Returns
    -------
    pandas.DataFrame
        The updated DataFrame with question marks replaced by 0.
    """
    df[col_name] = df[col_name].replace("?", 0)
    return df


def check_score_for_non_numeric(df, col_name):
    """
    Checks if a column of a DataFrame containing scores is numeric.
    If the column is not numeric, it tries to convert each value to a number and prints an error message if it fails.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    col_name : str
        The name of the column containing scores.

    Returns
    -------
    pandas.DataFrame
        The updated DataFrame with non-numeric scores replaced by NaN.
    """
    try:
        score_split = df[col_name].str.split(" - ", expand=True)
        if len(score_split.columns) == 2:
            df[["home_score", "away_score"]] = score_split.apply(pd.to_numeric)
        else:
            raise ValueError("Columns must be same length as key")
    except TypeError as err:
        console = Console()
        console.print(f"Non-numeric value(s) found in the '{col_name}' column: {err}")
        for index, x in df[col_name].iteritems():
            try:
                pd.to_numeric(x)
            except ValueError:
                print(
                    f"Non-numeric value found in row {index}, column '{col_name}': {x}")
    return df


def create_winner_column(df):
    """
    Creates a new column in a DataFrame indicating the winner of each match.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.

    Returns
    -------
    pandas.DataFrame
        The updated DataFrame with a new "winner" column.
    """
    df["winner"] = df.apply(lambda x: x["home_team"] if x["home_score"] > x["away_score"] else
                            x["away_team"] if x["home_score"] < x["away_score"] else
                            "draw", axis=1)
    return df


def compute_team_stats(df):
    """
    Computes various statistics for each team in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.

    Returns
    -------
    pandas.DataFrame
        A new DataFrame containing the computed statistics for each team.
    """
    return pd.DataFrame({"matches_played": df.groupby("home_team").size(),
                         "goals_scored": df.groupby("home_team")["home_score"].sum(),
                         "wins": ((df["home_team"] == df["winner"]).groupby(df["home_team"]).sum()
                                  + (df["away_team"] == df["winner"]).groupby(df["away_team"]).sum()),
                         "draws": ((df["home_score"] == df["away_score"]).groupby(df["home_team"]).sum()
                                   + (df["home_score"] == df["away_score"]).groupby(df["away_team"]).sum()),
                         "losses": ((df["home_team"] == df["away_team"]).groupby(df["home_team"]).size()
                                    - ((df["home_team"] == df["winner"]).groupby(df["home_team"]).sum()
                                       + (df["away_team"] == df["winner"]).groupby(df["away_team"]).sum())
                                    - ((df["home_score"] == df["away_score"]).groupby(df["home_team"]).sum()
                                       + (df["home_score"] == df["away_score"]).groupby(df["away_team"]).sum()))}).reset_index()


def plot_percentage_wins_losses_draws(team_stats_df):
    """
    Plots a bar chart showing the percentage of wins, draws, and losses for each team.

    Parameters
    ----------
    team_stats_df : pandas.DataFrame
        The DataFrame containing the team statistics.

    Returns
    -------
    None
    """
    fig, ax0 = plt.subplots(figsize=(10, 6))

    # Compute percentage of wins, losses, and draws for each team
    team_stats_df["wins_percentage"] = (
        team_stats_df["wins"] / team_stats_df["matches_played"]) * 50
    team_stats_df["draws_percentage"] = (
        team_stats_df["draws"] / team_stats_df["matches_played"]) * 50
    team_stats_df["losses_percentage"] = (
        team_stats_df["losses"] / team_stats_df["matches_played"]) * 50

    # Bar plot for percentage of wins, losses, and draws for each team
    ax0.bar(team_stats_df.index,
            team_stats_df["wins_percentage"], label="Wins")
    ax0.bar(team_stats_df.index, team_stats_df["draws_percentage"],
            bottom=team_stats_df["wins_percentage"], label="Draws")
    ax0.bar(team_stats_df.index, team_stats_df["losses_percentage"], bottom=team_stats_df[[
            "wins_percentage", "draws_percentage"]].sum(axis=1), label="Losses")

    # Add labels and legend
    ax0.set_title("Percentage of Wins, Draws, and Losses per Team")
    ax0.set_ylabel("Percentage")
    ax0.legend()

    # Add total number of games played as text above each bar
    for i, v in enumerate(team_stats_df["matches_played"]):
        ax0.text(i-0.2, v+1, str(v))
        ax0.tick_params(axis="x", labelsize=5)

    # Set square plot settings for top axis
    ax0.set_ylim([50, 5])

    # Set team names as x-axis labels
    ax0.set_xticks(team_stats_df.index)
    ax0.set_xticklabels(team_stats_df["home_team"])


def plot_total_goals_and_avg_score(matches_df):
    """
    Plots a scatter plot showing the total number of goals scored and the average score for each team.

    Parameters
    ----------
    matches_df : pandas.DataFrame
        The input DataFrame containing the match data.

    Returns
    -------
    None
    """
    # Compute average score for each team
    avg_score_df = pd.DataFrame({"avg_score": matches_df.groupby("home_team")["home_score"].mean() +
                                 matches_df.groupby("away_team")["away_score"].mean()}).reset_index()
    avg_score_df.columns = ["team", "avg_score"]

    # Compute total goals for each team
    total_goals_df = pd.DataFrame({"total_goals": matches_df.groupby("home_team")["home_score"].sum() +
                                   matches_df.groupby("away_team")["away_score"].sum()}).reset_index()
    total_goals_df.columns = ["team", "total_goals"]

    # Merge the two dataframes
    merged_df = pd.merge(avg_score_df, total_goals_df, on="team")

    # Bar chart for total goals
    fig, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(merged_df["team"], merged_df["total_goals"])
    ax2.set_ylabel("Total Goals")
    ax2.tick_params(axis="x", labelsize=5)

    # Line chart for average score
    fig, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(merged_df["team"], merged_df["avg_score"])
    ax3.set_ylabel("Average Score")
    ax3.tick_params(axis="x", labelsize=5)


if __name__ == "__main__":
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    plot_type = args.plot_type
    show_plot = args.show_plot

    # Load data
    matches_df = load_data(input_file)

    # Replace question marks in the scores column
    matches_df = replace_question_marks_with_zero(matches_df, "score")

    # Check for non-numeric values in the scores column
    matches_df = check_score_for_non_numeric(matches_df, "score")

    # Create winner column
    matches_df = create_winner_column(matches_df)

    # Compute team statistics
    team_stats_df = compute_team_stats(matches_df)

    if plot_type == "all" or plot_type == "percentage":
        # Plot percentage of wins, losses, and draws for each team
        plot_percentage_wins_losses_draws(team_stats_df)

    if plot_type == "all" or plot_type == "total_goals":
        # Plot total goals and average score for each team
        plot_total_goals_and_avg_score(matches_df)

    # Save output to file
    team_stats_df.to_csv(output_file, index=False)

    # Show plots
    if show_plot:
        plt.show()







