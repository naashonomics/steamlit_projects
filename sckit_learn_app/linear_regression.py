# Import required libraries

######## 1 #########

# streamlit
import streamlit as st


###### from 3 to final ######

# DS libraries
import pandas
from sklearn.linear_model import LinearRegression
import numpy
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

# title
st.title("Make predictions web app")

# user message
st.text("Please, upload your file in the side bar")

# button to start to analize
startAnalysis = st.sidebar.button("Start analysis")

######## 2 #########


# add upload file on sidebar
uploadFile = st.sidebar.file_uploader("Upload your excel file",type=["xlsx"])


######## 7 #########


# user to predict 
# (THIS IS GOING TO AFTER FINISHING THE FINAL PLOT)
# userToPredict = st.sidebar.number_input("To predict")

####################

# if start analausis
if startAnalysis:

    ##### copy jupyter notebook code HERE ####

    # data reading
    # import data
    dataset = pandas.read_excel(uploadFile)

    # test if it running correctly
    # print(dataset.shape)

    ######## 3 #########


    # add some user text
    st.info("Here is a description of your dataset")
    
    # get description
    # to say: write automatically how to display data (if it's text, dataset, or whatever)
    st.write(dataset.describe())

    st.info("Here is a plot to see distributions and correlations")

    # display the scatter matrix
    scatter_matrix(dataset, diagonal="hist")

    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    # display the plot
    st.pyplot()


    ######## 4 #########



    # train the model
    
    # get x and y
    # x = dataset.iloc[:,[ 0, 1, 2, 3]].values
    x = dataset.loc[:, ["Temperature"]]
    # x = dataset.iloc[:,[ 0]].values
    # y = dataset.iloc[:, -1].values
    y = dataset.loc[:, ["Power Electric"]]


    # create object model
    regressor = LinearRegression()

    # train model
    regressor.fit(x, y)

    # easy test
    # print("model fit ok")

    # data to predict
    xPredict = numpy.array([[
        # temperature
        19,

        ######## 7 #########

        # userToPredict,

        ####################

    ]])

    # do predictions
    prediction = regressor.predict(xPredict)[0]

    # user message
    st.success("Power electric generation prediction with temperature " + str(xPredict[0]) + " is: " + str(prediction))


    ######## 5 #########

    
    # user message
    st.info("Here you can see your data (blue), the model (red) and the prediction (yellow)")

    #create figure
    fig, ax = plt.subplots()

    # add lables to plots
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Power Electric")

    # dataset
    ax.scatter(x, y)

    # ploting the line
    ax.plot(x, regressor.intercept_[0] + regressor.coef_[0]*x, c="r")

    # plot prediction
    ax.scatter(xPredict, prediction, c="y", lineWidth=12)

    # display plot
    st.pyplot(fig)
