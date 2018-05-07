from   DeepSparseKernel  import np
import matplotlib.pyplot as plt
import sys
import DeepSparseKernel  as dsk

def trans(data):
    if data.ndim == 1:
        return data.reshape(data.size, 1)
    else:
        return data

train_x = trans(np.loadtxt('train_x')).T
train_y = trans(np.loadtxt('train_y'))
test_x  = trans(np.loadtxt('test_x')).T
test_y  = trans(np.loadtxt('test_y'))

dim, num_train = train_x.shape
num_obj        = train_y.shape[1]
num_test       = train_x.shape[1]

shared_layers_sizes     = [50, 50];
shared_activations      = [dsk.relu, dsk.tanh]
non_shared_layers_sizes = [50, 50];
non_shared_activations  = [dsk.relu, dsk.tanh]

shared_nn      = dsk.NN(shared_layers_sizes, shared_activations)
non_shared_nns = []

for i in range(num_obj):
    non_shared_nns += [dsk.NN(non_shared_layers_sizes, non_shared_activations)]

# def __init__(self, train_x, train_y, shared_nn, non_shared_nns, max_iter = 100, l1 = 0, l2 = 0, debug=False): 
modsk = dsk.MODSK(train_x, train_y, shared_nn, non_shared_nns, debug=True)

# random initialization of weights
scale = 0.1
theta = scale * np.random.randn(modsk.num_param)

# noises
for i in range(num_obj):
    theta[i]           = np.log(np.std(train_y[:, i]) / 2)
    theta[num_obj + i] = np.log(np.std(train_y[:, i]))
for i in range(dim):
    theta[2 * num_obj + i] = np.maximum(-100, np.log(0.5 * (train_x[i, :].max() - train_x[i, :].min())))

modsk.fit(theta)
print("Finished")