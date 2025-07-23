
# import pandas as pd
# import joblib

# from create_features import create_features  # make sure this file exists




# model_bat = joblib.load('/Users/tamoghnakumar/Desktop/fantasy_model_docker/model_batsman.pkl')
# model_bowl = joblib.load('/Users/tamoghnakumar/Desktop/fantasy_model_docker/model_bowler.pkl')

# with open('/Users/tamoghnakumar/Desktop/fantasy_model_docker/features_batsman.txt') as f:
#     features_bat = f.read().splitlines()

# with open('/Users/tamoghnakumar/Desktop/fantasy_model_docker/features_bowler.txt') as f:
#     features_bowl = f.read().splitlines()

# input_df = pd.read_csv('/Users/tamoghnakumar/Desktop/vs/my_env/players_input.csv', delimiter=';') 



# def map_player_ids(players_df, people_df):
#     players_df['normalized_name'] = players_df['Player Name'].str.lower().str.strip()
#     people_df['normalized_name'] = people_df['name'].str.lower().str.strip()

#     merged_df = players_df.merge(
#         people_df[['identifier', 'normalized_name']],
#         on='normalized_name',
#         how='left'
#     )

#     merged_df.rename(columns={'identifier': 'player_id'}, inplace=True)
#     merged_df.drop(columns=['normalized_name'], inplace=True)

#     return merged_df


# # Read people file
# people_df = pd.read_csv('/Users/tamoghnakumar/Desktop/people_naman.csv', delimiter=';')
# print(people_df.columns)

# # Filter input_df to only include players marked as PLAYING
# input_df = input_df[input_df['IsPlaying'].str.upper().str.strip() == 'PLAYING']

# # Map player IDs
# input_df = map_player_ids(input_df, people_df)

# print(input_df)
# print("Shape after filtering PLAYING:", input_df.shape)




# batsmen_df, bowlers_df  = create_features()
# # Select relevant features

# # X_bat = batsmen_df[features_bat]
# # X_bowl = bowlers_df[features_bowl]

# # # Predict
# # batsmen_df['predicted_score'] = model_bat.predict(X_bat)
# # bowlers_df['predicted_score'] = model_bowl.predict(X_bowl)

# # # Combine and sort
# # final_output = pd.concat([batsmen_df, bowlers_df]).sort_values(by='predicted_score', ascending=False)


# batsman_ids = set(batsmen_df['player_id'])
# bowler_ids = set(bowlers_df['player_id'])



# batsman_player_ids = []
# bowler_player_ids = []

# for player_id in input_df['player_id']:
#     if player_id in batsman_ids:
#         batsman_player_ids.append(player_id)
#     elif player_id in bowler_ids:
#         bowler_player_ids.append(player_id)

# # Get latest record per player
# latest_batsmen = batsmen_df[batsmen_df['player_id'].isin(batsman_player_ids)]
# latest_batsmen = latest_batsmen.sort_values('date').groupby('player_id').tail(1)

# latest_bowlers = bowlers_df[bowlers_df['player_id'].isin(bowler_player_ids)]
# latest_bowlers = latest_bowlers.sort_values('date').groupby('player_id').tail(1)

# # Select features
# X_bat = latest_batsmen[features_bat].fillna(0)
# X_bowl = latest_bowlers[features_bowl].fillna(0)

# print("Shape of X_bat:", X_bat.shape)
# print("Shape of X_bowl:", X_bowl.shape)

# print("\nX_bat head:")
# print(X_bat.head())
# print("\nX_bowl head:")
# print(X_bowl.head())

# if not X_bat.empty:
#     bat_player_ids_in_X = batsmen_df.loc[X_bat.index, 'player_id']
#     bat_predictions = model_bat.predict(X_bat)
#     bat_pred_df = pd.DataFrame({'player_id': bat_player_ids_in_X, 'predicted_bat_score': bat_predictions})
# else:
#     bat_pred_df = pd.DataFrame(columns=['player_id', 'predicted_bat_score']) 

# if not X_bowl.empty:
#     bowl_player_ids_in_X = bowlers_df.loc[X_bowl.index, 'player_id']
#     bowl_predictions = model_bowl.predict(X_bowl)
#     bowl_pred_df = pd.DataFrame({'player_id': bowl_player_ids_in_X, 'predicted_bowl_score': bowl_predictions})
# else:
#     bowl_pred_df = pd.DataFrame(columns=['player_id', 'predicted_bowl_score']) 

# output_df = input_df.copy()
# output_df = output_df.merge(bat_pred_df, on='player_id', how='left')
# output_df = output_df.merge(bowl_pred_df, on='player_id', how='left')

# # Initialize an empty DataFrame for final_players
# # Step 1: Select top player for each role and remove them from input/output_df
# final_players = pd.DataFrame(columns=output_df.columns)

# # Create predicted_score column based on whichever prediction is available
# output_df['predicted_score'] = output_df.apply(
#     lambda row: row['predicted_bat_score'] if pd.notnull(row['predicted_bat_score']) else row['predicted_bowl_score'],
#     axis=1
# )

# # Define roles
# roles = ['WK', 'BOWL', 'BAT', 'ALL']

# # Select top player from each role
# for role in roles:
#     top_player = output_df[output_df['Player Type'] == role].sort_values(
#         by='predicted_score', ascending=False
#     ).head(1)
    
#     if not top_player.empty:
#         final_players = pd.concat([final_players, top_player], ignore_index=True)

# # Drop these selected players from main DataFrames
# top_player_ids = final_players['player_id'].tolist()
# output_df = output_df[~output_df['player_id'].isin(top_player_ids)].reset_index(drop=True)
# input_df = input_df[~input_df['player_id'].isin(top_player_ids)].reset_index(drop=True)

# print(input_df)
# print(output_df)
# # Step 2: Define final score function and include final_players
# def calculate_final_score(input_df, final_players):
#     # Select top 6 batters and top 5 bowlers from the remaining input_df
#     top_batsmen = input_df.sort_values(by='predicted_bat_score', ascending=False).head(4)
#     top_bowlers = input_df.sort_values(by='predicted_bowl_score', ascending=False).head(3)

#     # Combine, deduplicate, and append final_players
#     top_players = pd.concat([top_batsmen, top_bowlers, final_players], ignore_index=True)
#     top_players = top_players.drop_duplicates(subset='player_id')

#     # Create predicted_score column if not present
#     if 'predicted_score' not in top_players.columns:
#         top_players['predicted_score'] = top_players.apply(
#             lambda row: row['predicted_bat_score'] if pd.notnull(row['predicted_bat_score']) else row['predicted_bowl_score'],
#             axis=1
#         )

#     # Sort for final ranking
#     top_players = top_players.sort_values(by='predicted_score', ascending=False).reset_index(drop=True)
    
#     return top_players

# # Step 3: Get the final selected squad
# final_team = calculate_final_score(output_df, final_players)


# # output_df['predicted_score'] = output_df.apply(calculate_final_score, axis=1)

# # final_output = output_df.sort_values(by='predicted_score', ascending=False)

# print(final_team)
# # Save or print
# # print(final_output[['player_name', 'role', 'predicted_score']])
# # final_output.to_csv('predictions_output.csv', index=False)


import pandas as pd
import joblib
from create_features import create_features  # make sure this file exists
import os

import sys

#Enter relevant match number here
match_number = 76




# if not (sys.version_info.major == 3 and sys.version_info.minor == 9):
#     sys.exit("❌ This script requires Python 3.9.x. Please run it with the correct version.")


try:
    dirname = os.path.dirname(os.path.abspath(__file__))
except NameError:
    dirname = os.getcwd()

model_bat = joblib.load(os.path.join(dirname, 'model_batsman.pkl'))
model_bowl = joblib.load(os.path.join(dirname, 'model_bowler.pkl'))

with open(os.path.join(dirname, 'features_batsman.txt')) as f:
    features_bat = f.read().splitlines()

with open(os.path.join(dirname, 'features_bowler.txt')) as f:
    features_bowl = f.read().splitlines()


def load_match_lineup(match_number):
    # Define path to Downloads folder
    downloads_path = os.path.expanduser("~/Downloads")
    # downloads_path="/Downloads"
    
    # Define full path to the Excel file
    file_path = os.path.join(downloads_path, "SquadPlayerNames_IndianT20League.xlsx")
    
    # Construct the tab (sheet) name
    sheet_name = f"Match_{match_number}"
    
    try:
        # Load the specific sheet into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    
    except FileNotFoundError:
        print("Excel file not found in Downloads folder.")
    except ValueError:
        print(f"Sheet '{sheet_name}' not found in the Excel file.")
    except Exception as e:
        print("An unexpected error occurred:", e)



lineup_df = load_match_lineup(match_number)

if lineup_df is not None:
    print(lineup_df.head())  # Display the first few rows

input_df=lineup_df

def map_player_ids(players_df, people_df):
    players_df['normalized_name'] = players_df['Player Name'].str.lower().str.strip()
    people_df['normalized_name'] = people_df['name'].str.lower().str.strip()

    merged_df = players_df.merge(
        people_df[['identifier', 'normalized_name']],
        on='normalized_name',
        how='left'
    )

    merged_df.rename(columns={'identifier': 'player_id'}, inplace=True)
    merged_df.drop(columns=['normalized_name'], inplace=True)

    return merged_df


# Read people file
people_df = pd.read_csv(os.path.join(dirname, 'people.csv'), delimiter=';')
print(people_df.columns)

# Filter input_df to only include players marked as PLAYING
input_df = input_df[input_df['IsPlaying'].str.upper().str.strip() == 'PLAYING']

# Map player IDs
input_df = map_player_ids(input_df, people_df)

print(input_df)
print("Shape after filtering PLAYING:", input_df.shape)

batsmen_df, bowlers_df  = create_features()

batsman_ids = set(batsmen_df['player_id'])
bowler_ids = set(bowlers_df['player_id'])

batsman_player_ids = []
bowler_player_ids = []

for player_id in input_df['player_id']:
    if player_id in batsman_ids:
        batsman_player_ids.append(player_id)
    elif player_id in bowler_ids:
        bowler_player_ids.append(player_id)

latest_batsmen = batsmen_df[batsmen_df['player_id'].isin(batsman_player_ids)]
latest_batsmen = latest_batsmen.sort_values('date').groupby('player_id').tail(1)

latest_bowlers = bowlers_df[bowlers_df['player_id'].isin(bowler_player_ids)]
latest_bowlers = latest_bowlers.sort_values('date').groupby('player_id').tail(1)

X_bat = latest_batsmen[features_bat].fillna(0)
X_bowl = latest_bowlers[features_bowl].fillna(0)

print("Shape of X_bat:", X_bat.shape)
print("Shape of X_bowl:", X_bowl.shape)

print("\nX_bat head:")
print(X_bat.head())
print("\nX_bowl head:")
print(X_bowl.head())

if not X_bat.empty:
    bat_player_ids_in_X = batsmen_df.loc[X_bat.index, 'player_id']
    bat_predictions = model_bat.predict(X_bat)
    bat_pred_df = pd.DataFrame({'player_id': bat_player_ids_in_X, 'predicted_bat_score': bat_predictions})
else:
    bat_pred_df = pd.DataFrame(columns=['player_id', 'predicted_bat_score']) 

if not X_bowl.empty:
    bowl_player_ids_in_X = bowlers_df.loc[X_bowl.index, 'player_id']
    bowl_predictions = model_bowl.predict(X_bowl)
    bowl_pred_df = pd.DataFrame({'player_id': bowl_player_ids_in_X, 'predicted_bowl_score': bowl_predictions})
else:
    bowl_pred_df = pd.DataFrame(columns=['player_id', 'predicted_bowl_score']) 

output_df = input_df.copy()
output_df = output_df.merge(bat_pred_df, on='player_id', how='left')
output_df = output_df.merge(bowl_pred_df, on='player_id', how='left')

final_players = pd.DataFrame(columns=output_df.columns)

output_df['predicted_score'] = output_df.apply(
    lambda row: row['predicted_bat_score'] if pd.notnull(row['predicted_bat_score']) else row['predicted_bowl_score'],
    axis=1
)

roles = ['WK', 'BOWL', 'BAT', 'ALL']

for role in roles:
    top_player = output_df[output_df['Player Type'] == role].sort_values(
        by='predicted_score', ascending=False
    ).head(1)
    
    if not top_player.empty:
        final_players = pd.concat([final_players, top_player], ignore_index=True)

# Drop these selected players from main DataFrames
top_player_ids = final_players['player_id'].tolist()
output_df = output_df[~output_df['player_id'].isin(top_player_ids)].reset_index(drop=True)
input_df = input_df[~input_df['player_id'].isin(top_player_ids)].reset_index(drop=True)

print(input_df)
print(output_df)
# Step 2: Define final score function and include final_players
def calculate_final_score(input_df, final_players):
    # Select top 6 batters and top 5 bowlers from the remaining input_df
    top_batsmen = input_df.sort_values(by='predicted_bat_score', ascending=False).head(5)
    top_bowlers = input_df.sort_values(by='predicted_bowl_score', ascending=False).head(2)

    # Combine, deduplicate, and append final_players
    top_players = pd.concat([top_batsmen, top_bowlers, final_players], ignore_index=True)
    top_players = top_players.drop_duplicates(subset='player_id')

    # Create predicted_score column if not present
    if 'predicted_score' not in top_players.columns:
        top_players['predicted_score'] = top_players.apply(
            lambda row: row['predicted_bat_score'] if pd.notnull(row['predicted_bat_score']) else row['predicted_bowl_score'],
            axis=1
        )

    # Sort for final ranking
    top_players = top_players.sort_values(by='predicted_score', ascending=False).reset_index(drop=True)
    
    return top_players

# Step 3: Get the final selected squad
# Step 3: Get the final selected squad
final_team = calculate_final_score(output_df, final_players)

# Add player_role column with default None
final_team['player_role'] = None

# Filter only eligible roles for captain/vice-captain
eligible_roles = ['BAT', 'WK', 'ALL']
eligible_players = final_team[final_team['Player Type'].isin(eligible_roles)]

# Sort by predicted_score to get top 2
top_two = eligible_players.sort_values(by='predicted_score', ascending=False).head(2)

# Assign captain and vice-captain
if len(top_two) > 0:
    final_team.loc[final_team['player_id'] == top_two.iloc[0]['player_id'], 'player_role'] = 'captain'
if len(top_two) > 1:
    final_team.loc[final_team['player_id'] == top_two.iloc[1]['player_id'], 'player_role'] = 'vicecaptain'

# Select final columns for output
cols = ['Player Name', 'Team', 'player_role']
final_team = final_team[cols]

# Save to CSV
downloads_path = "/Downloads"  # or use os.path.expanduser("~/Downloads")
team_name = "IITK_E5"  # ⬅️ change to your team name
output_filename = f"{team_name}_output.csv"
output_path = os.path.join(downloads_path, output_filename)

final_team.to_csv(output_path, index=False)

print(f"✅ Output saved to: {output_path}")













############ PREVIOUS CODE IN DOWNLOADS #####################

# import pandas as pd
# import joblib
# from create_features import create_features  # make sure this file exists
# import os

# import sys

# #Enter relevant match number here
# match_number = 76


# # if not (sys.version_info.major == 3 and sys.version_info.minor == 9):
# #     sys.exit("❌ This script requires Python 3.9.x. Please run it with the correct version.")


# try:
#     dirname = os.path.dirname(os.path.abspath(__file__))
# except NameError:
#     dirname = os.getcwd()

# model_bat = joblib.load(os.path.join(dirname, 'model_batsman.pkl'))
# model_bowl = joblib.load(os.path.join(dirname, 'model_bowler.pkl'))

# with open(os.path.join(dirname, 'features_batsman.txt')) as f:
#     features_bat = f.read().splitlines()

# with open(os.path.join(dirname, 'features_bowler.txt')) as f:
#     features_bowl = f.read().splitlines()


# def load_match_lineup(match_number):
#     # Define path to Downloads folder
#     downloads_path = os.path.expanduser("~/Downloads")
#     # downloads_path="/Downloads"
    
#     # Define full path to the Excel file
#     file_path = os.path.join(downloads_path, "SquadPlayerNames_IndianT20League.xlsx")
    
#     # Construct the tab (sheet) name
#     sheet_name = f"Match_{match_number}"
    
#     try:
#         # Load the specific sheet into a DataFrame
#         df = pd.read_excel(file_path, sheet_name=sheet_name)
#         return df
    
#     except FileNotFoundError:
#         print("Excel file not found in Downloads folder.")
#     except ValueError:
#         print(f"Sheet '{sheet_name}' not found in the Excel file.")
#     except Exception as e:
#         print("An unexpected error occurred:", e)



# lineup_df = load_match_lineup(match_number)

# if lineup_df is not None:
#     print(lineup_df.head())  # Display the first few rows

# input_df=lineup_df

# def map_player_ids(players_df, people_df):
#     players_df['normalized_name'] = players_df['Player Name'].str.lower().str.strip()
#     people_df['normalized_name'] = people_df['name'].str.lower().str.strip()

#     merged_df = players_df.merge(
#         people_df[['identifier', 'normalized_name']],
#         on='normalized_name',
#         how='left'
#     )

#     merged_df.rename(columns={'identifier': 'player_id'}, inplace=True)
#     merged_df.drop(columns=['normalized_name'], inplace=True)

#     return merged_df


# # Read people file
# people_df = pd.read_csv(os.path.join(dirname, 'people.csv'), delimiter=';')
# print(people_df.columns)

# # Filter input_df to only include players marked as PLAYING
# input_df = input_df[input_df['IsPlaying'].str.upper().str.strip() == 'PLAYING']

# # Map player IDs
# input_df = map_player_ids(input_df, people_df)

# print(input_df)
# print("Shape after filtering PLAYING:", input_df.shape)

# batsmen_df, bowlers_df  = create_features()

# batsman_ids = set(batsmen_df['player_id'])
# bowler_ids = set(bowlers_df['player_id'])

# batsman_player_ids = []
# bowler_player_ids = []

# for player_id in input_df['player_id']:
#     if player_id in batsman_ids:
#         batsman_player_ids.append(player_id)
#     elif player_id in bowler_ids:
#         bowler_player_ids.append(player_id)

# latest_batsmen = batsmen_df[batsmen_df['player_id'].isin(batsman_player_ids)]
# latest_batsmen = latest_batsmen.sort_values('date').groupby('player_id').tail(1)

# latest_bowlers = bowlers_df[bowlers_df['player_id'].isin(bowler_player_ids)]
# latest_bowlers = latest_bowlers.sort_values('date').groupby('player_id').tail(1)

# X_bat = latest_batsmen[features_bat].fillna(0)
# X_bowl = latest_bowlers[features_bowl].fillna(0)

# print("Shape of X_bat:", X_bat.shape)
# print("Shape of X_bowl:", X_bowl.shape)

# print("\nX_bat head:")
# print(X_bat.head())
# print("\nX_bowl head:")
# print(X_bowl.head())

# if not X_bat.empty:
#     bat_player_ids_in_X = batsmen_df.loc[X_bat.index, 'player_id']
#     bat_predictions = model_bat.predict(X_bat)
#     bat_pred_df = pd.DataFrame({'player_id': bat_player_ids_in_X, 'predicted_bat_score': bat_predictions})
# else:
#     bat_pred_df = pd.DataFrame(columns=['player_id', 'predicted_bat_score']) 

# if not X_bowl.empty:
#     bowl_player_ids_in_X = bowlers_df.loc[X_bowl.index, 'player_id']
#     bowl_predictions = model_bowl.predict(X_bowl)
#     bowl_pred_df = pd.DataFrame({'player_id': bowl_player_ids_in_X, 'predicted_bowl_score': bowl_predictions})
# else:
#     bowl_pred_df = pd.DataFrame(columns=['player_id', 'predicted_bowl_score']) 

# output_df = input_df.copy()
# output_df = output_df.merge(bat_pred_df, on='player_id', how='left')
# output_df = output_df.merge(bowl_pred_df, on='player_id', how='left')

# final_players = pd.DataFrame(columns=output_df.columns)

# output_df['predicted_score'] = output_df.apply(
#     lambda row: row['predicted_bat_score'] if pd.notnull(row['predicted_bat_score']) else row['predicted_bowl_score'],
#     axis=1
# )

# roles = ['WK', 'BOWL', 'BAT', 'ALL']

# for role in roles:
#     top_player = output_df[output_df['Player Type'] == role].sort_values(
#         by='predicted_score', ascending=False
#     ).head(1)
    
#     if not top_player.empty:
#         final_players = pd.concat([final_players, top_player], ignore_index=True)

# # Drop these selected players from main DataFrames
# top_player_ids = final_players['player_id'].tolist()
# output_df = output_df[~output_df['player_id'].isin(top_player_ids)].reset_index(drop=True)
# input_df = input_df[~input_df['player_id'].isin(top_player_ids)].reset_index(drop=True)

# print(input_df)
# print(output_df)
# # Step 2: Define final score function and include final_players
# def calculate_final_score(input_df, final_players):
#     # Select top 6 batters and top 5 bowlers from the remaining input_df
#     top_batsmen = input_df.sort_values(by='predicted_bat_score', ascending=False).head(5)
#     top_bowlers = input_df.sort_values(by='predicted_bowl_score', ascending=False).head(2)

#     # Combine, deduplicate, and append final_players
#     top_players = pd.concat([top_batsmen, top_bowlers, final_players], ignore_index=True)
#     top_players = top_players.drop_duplicates(subset='player_id')

#     # Create predicted_score column if not present
#     if 'predicted_score' not in top_players.columns:
#         top_players['predicted_score'] = top_players.apply(
#             lambda row: row['predicted_bat_score'] if pd.notnull(row['predicted_bat_score']) else row['predicted_bowl_score'],
#             axis=1
#         )

#     # Sort for final ranking
#     top_players = top_players.sort_values(by='predicted_score', ascending=False).reset_index(drop=True)
    
#     return top_players

# # Step 3: Get the final selected squad
# # Step 3: Get the final selected squad
# final_team = calculate_final_score(output_df, final_players)

# # Add player_role column with default None
# final_team['player_role'] = None

# # Filter only eligible roles for captain/vice-captain
# eligible_roles = ['BAT', 'WK', 'ALL']
# eligible_players = final_team[final_team['Player Type'].isin(eligible_roles)]

# # Sort by predicted_score to get top 2
# top_two = eligible_players.sort_values(by='predicted_score', ascending=False).head(2)

# # Assign captain and vice-captain
# if len(top_two) > 0:
#     final_team.loc[final_team['player_id'] == top_two.iloc[0]['player_id'], 'player_role'] = 'captain'
# if len(top_two) > 1:
#     final_team.loc[final_team['player_id'] == top_two.iloc[1]['player_id'], 'player_role'] = 'vicecaptain'

# # Select final columns for output
# cols = ['Player Name', 'Team', 'player_role']
# final_team = final_team[cols]

# # Save to CSV
# downloads_path = "/Downloads"  # or use os.path.expanduser("~/Downloads")
# team_name = "IITK_E5"  # ⬅️ change to your team name
# output_filename = f"{team_name}_output.csv"
# output_path = os.path.join(downloads_path, output_filename)

# final_team.to_csv(output_path, index=False)

# print(f"✅ Output saved to: {output_path}")
