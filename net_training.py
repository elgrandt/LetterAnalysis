import numpy as np
from scipy.optimize import fmin_bfgs,fmin_cg
from scipy.io import loadmat
import example_data, example_data2

def sigmoid(array):
    array = np.clip( array, -500, 500 )
    return 1.0 / (1.0 + np.exp(-array))

def sigmoidGradient(array):
    return sigmoid(array) * (1-sigmoid(array))

def forwardPropagation(thetas, X, n_examples):
    A = [np.concatenate((np.ones((n_examples,1)), X),1)]
    Z = [None]

    for x in range(len(thetas)):
        th = thetas[x]
        Z.append(np.matmul(A[x], np.transpose(th)))
        A.append(sigmoid(Z[x+1]))
        if x != len(thetas)-1:
            A[x+1] = np.concatenate((np.ones((n_examples,1)),A[x+1]),1)
    return A,Z

def Prediction(thetas, X, n_outputs):
    A,Z = forwardPropagation(thetas, X, X.shape[0])
    prediction = np.argmax(A[-1],1)
    res = []
    for x in prediction:
        act = np.zeros(n_outputs)
        act[x] = 1
        res.append(act)
    return np.array(res)

def CalculateJ(theta,X,y,theta_sizes):
    thetas = getRealThetas(theta,theta_sizes)
    del theta
    n_examples = X.shape[0]

    A,Z = forwardPropagation(thetas, X, n_examples)

    h = A[-1]
    np.clip(h,1e-20,1e20,out=h)
    h2 = 1-h
    np.clip(h2,1e-20,1e20,out=h2)
    #print(h)
    err = - y * np.log(h) - (1 - y) * np.log(h2)
    J = (1.0/n_examples) * sum(sum(err))

    del thetas,A,Z
    return J

def Gradient(theta,X,y,theta_sizes):
    thetas = getRealThetas(theta,theta_sizes)
    del theta

    n_examples = X.shape[0]
    A,Z = forwardPropagation(thetas, X, n_examples)
    h = A[-1]

    deltas = []
    deltas.append(np.transpose(h - y))
    for x in range(len(thetas)):
        if x != 0:
            break
        delta_act = np.matmul( np.transpose(thetas[len(thetas) - x - 1]), deltas[x] )
        delta_act = delta_act[1:]
        delta_act *= np.transpose( sigmoidGradient(Z[len(thetas) - x - 1]) )
        deltas.append(delta_act)
    deltas.append(None)
    deltas.reverse()

    DELTAS = []
    for x in range(len(A)-1):
        DELTAS.append( np.matmul( deltas[x+1], A[x] ) )
    DELTAS = np.array(DELTAS)

    grad = (1.0/n_examples) * DELTAS

    del thetas,deltas,DELTAS,A,Z,h
    return extendThetas(grad)


def extendThetas(thetas):
    theta = np.array([np.ravel(i) for i in thetas])
    theta = np.concatenate(theta)
    return theta

def getRealThetas(theta,theta_sizes):
    thetas = []
    act = 0
    for x in theta_sizes:
        thetas.append(np.reshape(theta[act:act + x[0] * x[1]],(x[0],x[1])))
        act += x[0] * x[1]
    thetas = np.array(thetas)
    return thetas

def train_neural_net(X,y):
    """
    :param X:
    Type: NP matrix
    Shape: (N of exampples, N of features)
    :param y:
    Type: NP matrix
    Shape: (N of exampels, N of outputs)
    :return:
    Optimal theta
    """
    hidden_layers = [25]

    """ SOME USEFUL DATA """
    n_examples = X.shape[0]
    n_features = X.shape[1]
    n_outputs = y.shape[1]
    n_hidden_layers = len(hidden_layers)

    """ GENERATING INITIAL THETAS """
    thetas = []
    theta_sizes = []
    Lin = n_features # Number of units of the layer at the left of actual theta
    for x in range(n_hidden_layers+1):
        if x < n_hidden_layers:
            Lout = hidden_layers[x] # Number of units of the layer at the right of actual theta
        else:
            Lout = n_outputs # Last layer
        epsilon = np.sqrt(6) / np.sqrt(Lin+Lout) # Range for random numbers
        thetas.append(np.random.rand(Lout, 1+Lin) * 2 * epsilon - epsilon)
        theta_sizes.append([Lout,1+Lin])
        if x < n_hidden_layers:
            Lin = hidden_layers[x]
    thetas = np.array(thetas)

    initial_theta = extendThetas(thetas)
    initial_theta = initial_theta.astype("float16")
    del thetas
    #print("Memory ussage:",initial_theta.shape[0] * initial_theta.shape[0] * initial_theta.dtype.itemsize, "Data type:", initial_theta.dtype)
    #print(CalculateJ(initial_theta,X,y,theta_sizes))
    #Gradient(initial_theta,X,y,theta_sizes)
    theta = fmin_cg(CalculateJ, initial_theta, fprime=Gradient, args=(X,y,theta_sizes), disp=True, maxiter=200)
    result = getRealThetas(theta,theta_sizes)

    """ TESTING EFFICIENCY """
    p = Prediction(result,X,n_outputs)
    prec = np.equal(p,y)
    p = 0
    for x in np.ravel(prec):
        if x:
            p += 1
    print(p/prec.size*100)
    return result

if __name__ == "__main__":
    data = loadmat("ex4data1.mat")
    y = []
    for x in data["y"]:
        act = np.zeros(10)
        act[x-1] = 1
        y.append(act)
    train_neural_net(data["X"],np.array(y))
    #train_neural_net(np.array(example_data.X,dtype=float),np.array(example_data.Y))