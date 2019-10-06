# CNN for activity type recognition
# More info:
# https://www.youtube.com/watch?v=grgNXdkmzzQ&list=PLnMKNibPkDnG9IC5Nl9vJg1CKMAO1kODW&index=3&t=0s

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras import optimizers
from sklearn.model_selection import train_test_split

random_seed = 611
np.random.seed( random_seed )

plt.style.use('ggplot')

# defining the function to plot a single axis data
def plotAxis( axis, x, y, title ):
    axis.plot( x, y )
    axis.set_title( title )
    axis.xaxis.set_visible( False )
    axis.set_ylim( [ min( y ) - np.std( y ), max( y ) + np.std( y ) ] )
    axis.set_xlim( [ min( x ), max( x ) ] )
    axis.grid( True )

# defining a function to plot the data for a given activity
def plotActivity( activity, data ):
    fig,( ax0, ax1, ax2 ) = plt.subplots( nrows = 3, figsize = ( 15, 10 ), sharex = True )
    plotAxis( ax0, data[ 'timestamp' ], data[ 'x-axis' ], 'x-axis' )
    plotAxis( ax1, data[ 'timestamp' ], data[ 'y-axis' ], 'y-axis' )
    plotAxis( ax2, data[ 'timestamp' ], data[ 'z-axis' ], 'z-axis' )
    plt.subplots_adjust( hspace = 0.2 )
    fig.suptitle( activity )
    plt.subplots_adjust( top = 0.9 )
    plt.savefig( activity + '.png' )
    plt.show()

# defining a window function for segmentation purposes
def windows( data, size ):
    start = 0
    while start < data.count():
        ### Good explanation about yield
        ### https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
        ### https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/
        yield int(start), int(start + size)
        start += ( size / 2 )

# segmenting the time series
def segment_signal( data, window_size = 90 ):
    segments = np.empty( ( 0, window_size, 3 ) ) ### Return a new array of given shape and type, without initializing entries.
    labels= np.empty( ( 0 ) )
    for ( start, end ) in windows( data[ 'timestamp' ], window_size ):
        x = data[ 'x-axis' ][ start : end ]
        y = data[ 'y-axis' ][ start : end ]
        z = data[ 'z-axis' ][ start : end ]
        if( len( data[ 'timestamp' ][ start : end ] ) == window_size ):
            segments = np.vstack( [ segments, np.dstack( [ x, y, z ] ) ] )
            # vstack - Stack arrays in sequence vertically (row wise).
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.vstack.html?highlight=vstack#numpy.vstack
            # dstack - Stack arrays in sequence depth wise (along third axis).
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.dstack.html?highlight=dstack#numpy.dstack
            labels = np.append( labels, stats.mode( data[ 'activity' ][ start : end ] )[ 0 ][ 0 ] )
    return segments, labels

### https://stackoverflow.com/questions/21546739/load-data-from-txt-with-pandas

columnNames = [ 'user_id', 'activity', 'timestamp', 'x-axis', 'y-axis', 'z-axis' ]
dataset = pd.read_csv( 'D://ITEA_Python_4_DataSci/CourseWork/HAR-CNN-Keras/actitracker_raw.txt', header = None, names=columnNames, na_values=';' )

# plotting a subset of the data to visualize
for activity in np.unique( dataset[ 'activity' ] ):
    subset = dataset[ dataset[ 'activity' ] == activity ][ : 180 ]
    plotActivity( activity, subset )

# segmenting the signal in overlapping windows of 90 samples with 50% overlap

segments, labels = segment_signal( dataset )

#categorically defining the classes of the activities

labels = np.asarray( pd.get_dummies( labels ), dtype = np.int8 )

# defining parameters for the input and network layers
# we are treating each segmeent or chunk as a 2D image (90 X 3)

numOfRows = segments.shape[ 1 ]
numOfColumns = segments.shape[ 2 ]
numFilters = 128 # number of filters in Conv2D layer
# kernal size of the Conv2D layer
kernalSize1 = 2
# max pooling window size
poolingWindowSz = 2
# number of filters in fully connected layers
numNueronsFCL1 = 128
numNueronsFCL2 = 128
# split ratio for test and validation
trainSplitRatio = 0.8
# number of epochs
Epochs = 10
# batchsize
batchSize = 10
# number of total clases
numClasses = labels.shape[1]
# dropout ratio for dropout layer
dropOutRatio = 0.2
# reshaping the data for network input
reshapedSegments = segments.reshape( segments.shape[ 0 ] , numOfRows, numOfColumns, 1 )
# splitting in training and testing data
trainSplit = np.random.rand( len( reshapedSegments ) ) < trainSplitRatio
trainX = reshapedSegments[ trainSplit ]
testX = reshapedSegments[ ~trainSplit ]
trainX = np.nan_to_num( trainX )
testX = np.nan_to_num( testX )
trainY = labels[ trainSplit ]
testY = labels[ ~trainSplit ]

# train_X, test_X, train_y, test_y = train_test_split( X, y, test_size = 0.2, random_state = 42 )

model = Sequential()
# adding the first convolutionial layer with 32 filters and 5 by 5 kernal size, using the rectifier as the activation function
model.add( Conv2D( numFilters, ( kernalSize1, kernalSize1 ), input_shape = ( numOfRows, numOfColumns, 1 ), activation = 'relu' ) )
# adding a maxpooling layer
model.add( MaxPooling2D( pool_size = ( poolingWindowSz, poolingWindowSz ), padding = 'valid' ) )
# adding a dropout layer for the regularization and avoiding over fitting
model.add( Dropout( dropOutRatio ) )
# flattening the output in order to apply the fully connected layer
model.add( Flatten() )
# adding first fully connected layer with 256 outputs
model.add( Dense( numNueronsFCL1, activation = 'relu' ) )
#adding second fully connected layer 128 outputs
model.add( Dense( numNueronsFCL2, activation = 'relu' ) )
# adding softmax layer for the classification
model.add( Dense( numClasses, activation = 'softmax' ) )
# Compiling the model to generate a model
adam = optimizers.Adam( lr = 0.001, decay = 1e-6 )
model.compile( loss = 'categorical_crossentropy', optimizer = adam, metrics = [ 'accuracy' ] )

for layer in model.layers:
    print( layer.name )

model.fit( trainX, trainY, validation_split = 1 - trainSplitRatio, epochs = Epochs, batch_size = batchSize, verbose = 2 )
score = model.evaluate( testX, testY, verbose = 2 )
print( 'Baseline Error: %.2f%%' % ( 100 - score[ 1 ] * 100 ) )
# model.save('model.h5')
# np.save('groundTruth.npy',testY)
# np.save('testData.npy',testX)
