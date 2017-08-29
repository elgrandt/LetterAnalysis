import numpy as np
from scipy.optimize import fmin_bfgs
import example_data

def sigmoid(array):
    array = np.clip( array, -500, 500 )
    return 1.0 / (1.0 + np.exp(-array))

def CalculateJ(theta,X,y,theta_sizes):
    thetas = GetRealThetas(theta,theta_sizes)
    n_examples = X.shape[0]

    A = [np.concatenate((np.ones((n_examples,1)), X),1)]
    Z = [None]

    for x in range(len(thetas)):
        th = thetas[x]
        Z.append(np.matmul(A[x], np.transpose(th)))
        A.append(sigmoid(Z[x+1]))
        if x != len(thetas)-1:
            A[x+1] = np.concatenate((np.ones((n_examples,1)),A[x+1]),1)

    h = A[-1]
    err = - y * np.log(h) - (1 - y) * np.log(1-h)
    J = (1.0/n_examples) * sum(sum(err))
    print(J)
    return J

def Gradient(theta,X,y,theta_sizes):
    thetas = GetRealThetas(theta,theta_sizes)

def ExtendThetas(thetas):
    theta = np.array([np.ravel(i) for i in thetas])
    theta = np.concatenate(theta)
    return theta

def GetRealThetas(theta,theta_sizes):
    thetas = []
    act = 0
    for x in theta_sizes:
        thetas.append(np.reshape(theta[act:act + x[0] * x[1]],(x[0],x[1])))
        act += x[0] * x[1]
    thetas = np.array(thetas)
    return thetas

#-1,-6
def train_neural_net(X,y):
    """
    :param X:
    Type: NP array
    Size: (N of exampples, N of features)
    :param y:
    Type: NP array
    Size: (N of exampels, N of outputs)
    :return:
    Optimal theta
    """
    hidden_layers = [50]

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

    initial_theta = ExtendThetas(thetas)
    #CalculateJ(initial_theta,X,y,theta_sizes)
    theta = fmin_bfgs(CalculateJ, initial_theta, args=(X,y,theta_sizes), maxiter=50, disp=True)
    print(theta)

if __name__ == "__main__":
    train_neural_net(np.array(example_data.X,dtype=float),np.array(example_data.Y))