import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.font_manager as font_manager
from io import BytesIO


# Load the data
df = pd.read_csv('countywithswingpercentages_updated.csv', low_memory=False)
df['Game'] = df['Match'] + ' ' + df['Date']

# Create a list of unique batter names
batter_names = df['Batter'].unique().tolist()

# Define the function to plot
def batter_plot(batter_name, player_game='Season', player_inning='Game'):
    df1 = df[df['Batter'] == batter_name]
    player_games = df1['Game'].unique().tolist()
    player_games.append('Season')  # Add 'Season' option to the game list
    
    innings_list = []  # Initialize innings_list as an empty list
    if player_game and player_game != 'Season':
        df1 = df1[df1['Game'] == player_game]
        innings_list = df1['Innings'].unique().tolist()  
        innings_list.append('Game')  # Add default 'Game' option
    
    if player_inning and player_inning != 'Game':
        df1 = df1[df1['Innings'] == player_inning]

    background_colour = '#d0f7e3'
    font_path = 'Arvo-Regular.ttf'
    font_props = font_manager.FontProperties(fname=font_path)
    
    fig = plt.figure(figsize=(8, 12))
    fig.patch.set_facecolor(background_colour)

    # Text and scatter plots as in your original code
    ax1 = fig.add_axes([0, 0.7, 1, 0.2])
    ax1.set_facecolor(background_colour)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    
    ax1.text(x=0.5, y=0.85, s=batter_name, fontsize=20, fontproperties=font_props, fontweight='bold', color='black', ha='center')
    ax1.text(x=0.5, y=0.73, s='Balls Faced in County Championship 2024' if player_game=='Season' else 'Balls Faced in '+str(player_game)+' in the '+str(player_inning), fontsize=14, fontproperties=font_props, fontweight='bold', color='black', ha='center')
    ax1.text(x=0.25, y=0.5, s='Less Played At', fontsize=12, fontproperties=font_props, fontweight='bold', color='black', ha='center')

    ax1.scatter(x=0.37, y=.53, s=100, color=background_colour, edgecolor='black', linewidth=0.8)
    ax1.scatter(x=0.42, y=.53, s=200, color=background_colour, edgecolor='black', linewidth=0.8)
    ax1.scatter(x=0.48, y=.53, s=300, color=background_colour, edgecolor='black', linewidth=0.8)
    ax1.scatter(x=0.54, y=.53, s=400, color=background_colour, edgecolor='black', linewidth=0.8)
    ax1.scatter(x=0.6, y=.53, s=500, color=background_colour, edgecolor='black', linewidth=0.8)
    ax1.text(x=0.75, y=0.5, s='More Played At', fontsize=12, fontproperties=font_props, fontweight='bold', color='black', ha='center')

    ax1.text(x=0.45, y=0.27, s='Played At', fontsize=10, fontproperties=font_props, fontweight='bold', color='black', ha='right')
    ax1.scatter(x=0.47, y=.3, s=100, color='blue', edgecolor='black', linewidth=0.8, alpha=.7)
    ax1.scatter(x=0.53, y=.3, s=100, color=background_colour, edgecolor='black', linewidth=0.8, alpha=.7)

    ax1.text(x=0.55, y=0.27, s='Not Played At', fontsize=10, fontproperties=font_props, fontweight='bold', color='black', ha='left')


    ax1.text(x=0.75, y=0.5, s='More Played At', fontsize=12, fontproperties=font_props, fontweight='bold', color='black', ha='center')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)

    # Turn off the axis (including ticks and labels)
    ax1.set_axis_off()
    # Main plot
    ax2 = fig.add_axes([0.05, 0.25, 0.9, 0.5])
    ax2.set_facecolor(background_colour)
    
    for x in df1.to_dict(orient='records'):
        ax2.scatter(x['PastY'], x['PastZ'], s=300*x['Swing Percentage'], color=background_colour if x['Shot'] in ['Back Defence', 'No Shot', 'Forward Defence', 'Padded Away'] else 'blue', alpha=0.7, linewidth=.8, edgecolor='black')
    
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(0, 2)

    image_path = 'stumps copy.png'
    img = mpimg.imread(image_path)
    ax2.imshow(img, extent=[-0.1143, 0.1143, 0, 0.72], aspect='auto', zorder=-1, alpha=0.7)

    ax2.set_axis_off()
    
    balls = df1.shape[0]
    runs = df1['Runs'].sum()
    
    df2 = df1[~df1['Shot'].isin(['Back Defence', 'No Shot', 'Forward Defence', 'Padded Away'])]
    average_swing_percentage_of_swings = df2['Swing Percentage'].sum()/df2.shape[0]

    swing_percentage = df2.shape[0]/df1.shape[0]

    df4 = df1[df1['Swing Percentage']<0.1]
    df5 = df4[~df4['Shot'].isin(['Back Defence', 'No Shot', 'Forward Defence', 'Padded Away'])]
    if df4.shape[0] ==0:
        rare_swing_percentage = 0
    else:
        rare_swing_percentage = df5.shape[0]/df4.shape[0]

    ax3 = fig.add_axes([0,0.2,1,0.05]) #Bottom left corner, width, height going to start
    ax3.set_facecolor(background_colour)
    
    ax3.text(x=.1, y=.2, s='Balls', fontsize=20, fontproperties=font_props, fontweight='bold', color='black', ha='left')
    ax3.text(x=.1, y=-0.3, s=f'{balls}', fontsize=16, fontproperties=font_props, color='blue', ha='left')


    ax3.text(x=.25, y=.2, s='ASPS', fontsize=20, fontproperties=font_props, fontweight='bold', color='black', ha='left')
    ax3.text(x=.25, y=-0.3, s=f'{average_swing_percentage_of_swings:.2f}', fontsize=16, fontproperties=font_props, color='blue', ha='left')

    ax3.text(x=.4, y=.2, s='Shot %', fontsize=20, fontproperties=font_props, fontweight='bold', color='black', ha='left')
    ax3.text(x=.4, y=-0.3, s=f'{swing_percentage:.2f}', fontsize=16, fontproperties=font_props, color='blue', ha='left')

    ax3.text(x=.56, y=.2, s='Rare Swing %', fontsize=20, fontproperties=font_props, fontweight='bold', color='black', ha='left')
    ax3.text(x=.56, y=-0.3, s=f'{rare_swing_percentage:.2f}', fontsize=16, fontproperties=font_props, color='blue', ha='left')

    ax3.text(x=.82, y=.2, s='Runs', fontsize=20, fontproperties=font_props, fontweight='bold', color='black', ha='left')
    ax3.text(x=.82, y=-0.3, s=f'{runs}', fontsize=16, fontproperties=font_props, color='blue', ha='left')

    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)

    # Turn off the axis (including ticks and labels)
    ax3.set_axis_off()

    #plt.savefig("/Users/jamesbrooker/Documents/plots/" + batter_name + ".png", format='png', dpi=300)
    
    return player_games, innings_list, fig

# Streamlit app
def main():
    st.title("Batter Performance Plotter")
    
    # Step 1: Select the batter
    batter_name = st.selectbox("Select Batter", batter_names)

    if batter_name:
        # Step 2: Get the list of games for the selected batter
        player_games, innings_list, fig = batter_plot(batter_name)
        
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format="png")
        img_buffer.seek(0)
        
        # Step 3: Select the game
        player_game = st.selectbox("Select Game", player_games)
        
        # Step 4: Dynamically update innings based on game selection
        if player_game != 'Season':
            innings_list = df[df['Batter'] == batter_name]
            innings_list = innings_list[innings_list['Game'] == player_game]['Innings'].unique().tolist()
            innings_list.append('Game')  # Add 'Game' option if not Season
        else:
            innings_list = ['Game']

        # Step 5: Select the inning
        player_inning = st.selectbox("Select Inning", innings_list)
        
        # Step 6: Display the plot after game and inning selection
        if st.button("Plot"):
            batter_plot(batter_name, player_game, player_inning)
            st.image(img_buffer, caption=f"{batter_name}'s Plot", use_column_width=True)

if __name__ == '__main__':
    main()
