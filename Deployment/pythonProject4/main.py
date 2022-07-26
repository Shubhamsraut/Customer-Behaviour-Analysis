import pickle
import streamlit as st
import webbrowser
from PIL import Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# import plotly.express as px
# import pandas as pd
# loading the trained model
pickle_in = open ( 'RFC_model_1.pkl', 'rb' )
classifier = pickle.load ( pickle_in )

st.sidebar.title ( "Menu" )
st.title ( "Customer's Personality Analysis" )
image = Image.open ( 'CBA.png' )
st.image ( image )

menu = st.sidebar.checkbox ( 'Options' )
# @st.cache()
if menu:
    # defining the function which will make the prediction using the data which the user inputs
    def prediction(Education, Living_With, Children, Family_Size, AgeGroup, Join_year, Incomes, Total_num_purchase,
                   Total_accept, Expense):
        # Pre-processing user input

        if Education == "Undergraduate":
            Education = 0

        elif Education == "Graduated":
            Education = 1

        elif Education == "Postgraduated":
            Education = 2

        # *****************************************#

        if Living_With == "Alone":
            Living_With = 0

        elif Living_With == "Partner":
            Living_With = 1

        # *****************************************#
        if Incomes == "Below 25000":
            Incomes = 0

        elif Incomes == "Between 25000-50000":
            Incomes = 1

        elif Incomes == "Between 50000-100000":
            Incomes = 2

        elif Incomes == "Above 100000":
            Incomes = 3

        # *****************************************#

        if Family_Size == "0":
            Family_Size = 0

        elif Family_Size == "1":
            Family_Size = 1

        elif Family_Size == "2":
            Family_Size = 2

        elif Family_Size == "3":
            Family_Size = 3

        elif Family_Size == "4":
            Family_Size = 4

        # *****************************************#

        if Children == "0":
            Children = 0

        elif Children == "1":
            Children = 1

        elif Children == "2":
            Children = 2

        elif Children == "3":
            Children = 3

        # *****************************************#
        if Join_year == "2012":
            Join_year = 2012

        elif Join_year == "2013":
            Join_year = 2013

        elif Join_year == "2014":
            Join_year = 2014

        # *****************************************#

        if AgeGroup == "13 - 19 --> Teen":
            AgeGroup = 0

        elif AgeGroup == "20 - 39 --> Adult":
            AgeGroup = 1

        elif AgeGroup == "40 - 59 --> Middle Age Adult":
            AgeGroup = 2

        elif AgeGroup == "More than 60 --> Senior Adult ":
            AgeGroup = 3

        # *****************************************#

        if Expense == "Below 500":
            Expense = 0

        elif Expense == "Between 500-1000":
            Expense = 1

        elif Expense == "Above 1000":
            Expense = 2

        # *****************************************#

        prediction = classifier.predict (
            [[Education, Living_With, Children, Family_Size, AgeGroup, Join_year, Incomes, Total_num_purchase,
              Total_accept,
              Expense]] )

        pred_1 = 0
        if prediction == 0:
            pred_1 = 'cluster 0'

        elif prediction == 1:
            pred_1 = 'cluster 1'

        elif prediction == 2:
            pred_1 = 'cluster 2'

        elif prediction == 3:
            pred_1 = 'cluster 3'

        return pred_1


    # this is the main function in which we define our webpage
    def main():
        # front end elements of the web page
        html_temp = """ 
            <div style ="background-color:Green;padding:13px"> 
            <h1 style ="color:black;text-align:center;">Model Deployment</h1> 
            </div> 
            """

        # display the front end aspect
        st.markdown ( html_temp, unsafe_allow_html=True )

        # following lines create boxes in which user can enter data required to make prediction

        Education = st.selectbox ( "Education", ("Undergraduate", "Graduated", "Postgraduated") )

        Living_With = st.radio ( "Living_With: ", ('Alone', 'Partner') )
        if (Living_With == 'Alone'):
            st.success ( "Alone" )
        elif (Living_With == 'Partner'):
            st.success ( "Partner" )

        Children = st.selectbox("Number of Childrens", ("0", "1", "2", "3", "4"))

        Family_Size = st.selectbox("Family_Size", ("0", "1", "2", "3", "4", "5"))

        AgeGroup = st.selectbox ( "AgeGroup", (
            "13 - 19 --> Teen", "20 - 39 --> Adult", "40 - 59 --> Middle Age Adult", "More than 60 --> Senior Adult ") )

        Join_year = st.selectbox ( "Join_year", ("2012", "2013", "2014") )

        Incomes = st.selectbox ( "Incomes",
                                 ("Below 25000", "Between 25000-50000", "Between 50000-100000", "Above 100000") )

        Total_accept = st.slider ( "Number of accepted campain", 0, 10 )
        st.text ( 'Selected: {}'.format ( Total_accept ) )

        Total_num_purchase = st.slider ( "Number of Purchase Made", 0, 50 )
        st.text ( 'Selected: {}'.format ( Total_num_purchase ) )

        Expense = st.selectbox ( "Expense", ("Below 500", "Between 500-1000", "Above 1000") )

        result = ""

        # initialize session state
        if "load_state" not in st.session_state:
            st.session_state.load_state = False

        # when 'Predict' is clicked, make the prediction and store it
        if st.button ( "Predict" ):
            result = prediction ( Education, Living_With, Children, Family_Size, AgeGroup, Join_year, Incomes,
                                  Total_num_purchase, Total_accept, Expense )
        st.success ( 'Common cluster is {}'.format ( result ) )

        # *************************************#
        Data = pickle.load ( open ( 'customers.pkl', 'rb' ) )
        customers = pd.DataFrame ( Data )
        st.markdown ( "We can have a Quick Analysis Based on the Options you choose" )
        if st.button ( "Analysis" ) or st.session_state.load_state:
            st.session_state.load_state = True
            radio = st.radio ( "Charts", ("Join Weekday", "Join Month", "Complain") )
            if radio == "Join Weekday":
                bar_week = pd.DataFrame ( customers ['Join_weekday'] )
                fig_hist = plt.figure ( figsize=(10, 5) )
                sns.histplot ( data=bar_week, x='Join_weekday', color='olive' )
                plt.title ( "Histogram For Weekday" )
                st.pyplot ( fig_hist )
            elif radio == "Join Month":
                bar_month = pd.DataFrame ( customers ['Join_month'] )
                fig_hist = plt.figure ( figsize=(10, 5) )
                sns.histplot ( data=bar_month, x='Join_month', color='forestgreen' )
                plt.title ( "Histogram For Month" )
                st.pyplot ( fig_hist )
            else:
                bar_complain = pd.DataFrame ( customers ['Complain'] )
                fig_hist = plt.figure ( figsize=(10, 5) )
                sns.histplot ( data=bar_complain, x='Complain', bins=3, color='firebrick' )
                plt.title ( "Histogram For Complains" )
                st.pyplot ( fig_hist )
            # Histogram
            radio_1 = st.radio ( "Uni-Variate", ("Education, Living With, Children, Join Year", "Age Group, Expense, Total Accept, Incomes",
            "Family Size, Total Number of Purchases") )
            if radio_1 == "Education, Living With, Children, Join Year":
                visual = pd.DataFrame ( customers, columns=['Education', 'Living_With', 'Children', 'Join_year'] )
                visual.hist ()
                plt.show ()
                st.pyplot ( plt )
            elif radio_1 == "Age Group, Expense, Total Accept, Incomes":
                visual = pd.DataFrame ( customers, columns=['AgeGroup', 'Expense', 'Total_accept', 'Incomes'] )
                visual.hist ()
                plt.show ()
                st.pyplot ( plt )
            else:
                visual = pd.DataFrame ( customers, columns=['Family_Size', 'Total_num_purchase'] )
                visual.hist ()
                plt.show ()
                st.pyplot ( plt )
            visual = pd.DataFrame ( customers [:50], columns=['Living_With', 'Join_month', 'Complain'] )
            st.line_chart ( visual )


    if __name__ == '__main__':
        main ()

about = 'http://localhost:8502'
if st.sidebar.button ('About System'):
    webbrowser.open_new_tab ( about )

Dataset = 'http://localhost:8503'
if st.sidebar.button ("Dataset"):
    webbrowser.open_new_tab ( Dataset )


