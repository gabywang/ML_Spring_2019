import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import tarfile
from six.moves import urllib

from sklearn.linear_model import LinearRegression
from sklearn import linear_model

from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

from matplotlib import animation
from IPython.display import HTML

import random 

class TrainingModelsHelper():
    DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
    HOUSING_PATH = os.path.join("datasets", "housing")
    HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

    def __init__(self, **params):
       
        return

  
    def fetch_housing_data(self, housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
        if not os.path.isdir(housing_path):
            os.makedirs(housing_path)
        tgz_path = os.path.join(housing_path, "housing.tgz")
        urllib.request.urlretrieve(housing_url, tgz_path)
        housing_tgz = tarfile.open(tgz_path)
        housing_tgz.extractall(path=housing_path)
        housing_tgz.close()



    def load_housing_data(self, housing_path=HOUSING_PATH):
        csv_path = os.path.join(housing_path, "housing.csv")

        # Get data from cache is available
        if os.path.isfile(csv_path):
            return pd.read_csv(csv_path)
        else:
            # Download it
            self.fetch_housing_data()
            return pd.read_csv(csv_path)

class GradientDescentHelper():
    def __init__(self, **params):
        return

    def gen_lr_data(self, seed=42):
        np.random.seed(seed)

        X = 2 * np.random.rand(100, 1)
        y = 4 + 3 * X + np.random.randn(100, 1)

        return X,y

    def fit_lr(self, X, y):
        lin_reg = LinearRegression()
        lin_reg.fit(X, y)

        return lin_reg

    def plot_lr(self, X, y, model, xlabel="feature", ylabel="target"):
        # Plot predicted ylabel (red) and true label (black)
        fig = plt.figure()
        ax  = fig.add_subplot(1,1,1)

        # Predict
        y_pred = model.predict(X)

        # Scatter plot of actual and predicted
        _ = ax.scatter(X[:,0], y,      color='black')
        _ = ax.scatter(X[:,0], y_pred, color="red")

        # Plot fit
        on_idx = 0
        sort_idx = X[:, on_idx].argsort()
        X_sorted = X[ sort_idx,:]
        y_pred_sorted = y_pred[ sort_idx,:]
    
        _ = ax.plot(X_sorted[:, on_idx] , y_pred_sorted, color="red")
       
        _ = ax.set_xlabel(xlabel)
        _ = ax.set_ylabel(ylabel)

        return fig, ax


    def batchGradientDescent_lr(self, X, y, eta=0.1, n_iterations=1000, seed=42):
        m = X.shape[0]

        # Add intercept feature
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # add x0 = 1 to each instance


        np.random.seed(seed)

        theta = np.random.randn( X_b.shape[-1],1)

        for iteration in range(n_iterations):
            gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
            theta = theta - eta * gradients

        return theta

    def predict(self, X, theta):
        # Add intercept feature
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # add x0 = 1 to each instance
        
        y_predict = X_b.dot(theta)

        return y_predict

    def make_movie(self, X, y, eta=0.1 , 
              seed=42, 
              n_iterations=1000,
              theta_path=None):


        # Min/Max X, for plotting fitted line
        X_new = np.array( [ np.round(X.min(), 0), np.round(X.max()) ]).reshape(-1,1)

        X_b = np.c_[np.ones((len(X), 1)), X]  # add x0 = 1 to each instance
        plots = []

        np.random.seed(seed)
        theta = np.random.randn(2,1)  # random initialization

        X_new_b = np.c_[np.ones((2, 1)), X_new]  # add x0 = 1 to each instance
        m = len(X_b)

        
        for iteration in range(n_iterations):
            if iteration % 1 == 0:
                # Predict at min/max values of X, save predictions
                y_predict = X_new_b.dot(theta)
                plots.append( (X_new, y_predict) )

            gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
            theta = theta - eta * gradients
            if theta_path is not None:
                theta_path.append(theta)

        return theta, plots

    def def_init(self, X, y, title=None):
        # First set up the figure, the axis, and the plot element we want to animate
        plt.ioff()
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 2), ylim=(0,11))

        if title is not None:
            ax.set_xlabel(title)
        
        line, = ax.plot([], [], lw=2)
        scatter, = ax.plot(X, y, "b.")

        self.fig, self.ax, self.line = fig, ax, line

        def init():
            # plt.plot(X, y, "b.")
            line.set_data([], [])
            line.set_linestyle("-")

            plt.show()
            return line,
        
        return init

    def def_animate(self, movie):
        ax, line = self.ax, self.line

        def animate(i):
            p = movie[i]
            x, y = p

            ax.set_title("Iteration = {s:d}".format(s=i) )

            line.set_data(x, y)
            line.set_linestyle("-")

            return line,

        return animate

    def create_movie(self, X, y, eta=0.1, n_iterations=1000, interval=2000):
        # Create the frames
        theta, movie = self.make_movie(X, y, eta=eta, n_iterations=n_iterations, theta_path=None)

        self.movie = movie

        # self.def_init creates attributes of self that are required for other methods, e.g, self.fig, self.movie
        init_func = self.def_init(X, y, title="Eta = {e:.2f}".format(e=eta) )
        animate_func = self.def_animate(movie)
        
        fig = self.fig

        anim = animation.FuncAnimation(fig, animate_func, init_func=init_func,
                               frames=len(movie), interval=interval, blit=True)

        return anim

    def show_movie(self, anim):
        return HTML(anim.to_html5_video())


class InfluentialHelper():
    def __init__(self, **params):
        return

    def gen_data(self, num=10, seed=42):
        rng = np.random.RandomState(seed)
        x = np.linspace(-10, 10, num).reshape(-1,1)
        y =  x + rng.normal(size=num).reshape(-1,1)

        return(x,y)

    def setup(self, num=10):
        (x,y) = self.gen_data(num)
        self.x, self.y = x, y

        return x,y

    def fit(self, x,y):
        regr = linear_model.LinearRegression()
        regr.fit(x,y)
        y_pred = regr.predict(x)
        return (x, y_pred, regr.coef_[0])


    def plot_update(self, x,y, fitted):
        fig = plt.figure()
        ax  = fig.add_subplot(1,1,1)
        plt.ion()

        _ = ax.scatter(x, y, color='black', label="true")
        ax.plot( fitted[0], fitted[1], color='red', label='fit')

        slope = fitted[2]

        ax.set_title("Slope = {s:.2f}".format(s=slope[0]))
        # count += 1
        # if count % max_count == 0:
        fig.canvas.draw()


    def def_update(self):
        x, y = self.x, self.y

        def fit_update(x_l, y_l):
            x_update, y_update = x.copy(), y.copy()
            y_update[ x_l ] = y_l

            fitted = self.fit(x_update,y_update)
            self.plot_update(x_update, y_update, fitted)

        return fit_update

    def show_slider(self, num=10):
        x, y = self.x, self.y
        update_func = self.def_update()

        interact(update_func,
                 x_l=widgets.IntSlider(min=0, max=num-1, step=1,value=int(num/2),     continous_update=False),
                 y_l=widgets.IntSlider(min=y.min(),max=y.max(),step=1, value=y[ int(num/2)], continous_update=False)
                    );

class KNN_Helper():
    """
    Derived from: https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
    # Code source: Gaël Varoquaux
    #              Andreas Müller
    # Modified for documentation by Jaques Grobler
    # License: BSD 3 clause
    """

    def __init__(self, **params):
        self.names = ["Nearest Neighbors", 
                      "Decision Tree", "Random Forest"]

        self.classifiers = [
            KNeighborsClassifier(3),
            DecisionTreeClassifier(max_depth=5),
            RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
            ]

        self.cm = plt.cm.RdBu
        self.cm_bright = ListedColormap(['#FF0000', '#0000FF'])

        return

    def stretch_ds(self, ds, mag):
        """
        Stretch a dataset by scaling the features

        Parameters
        ----------
        ds: Tuple (X,y)
        - X are the features, y are the targets
        -- X: ndarray.   Two dimensional

        mag: ndarray. One dimensional.  Length matches second dimension of X

        Returns
        --------
        Xprime: ndarray
        - same dimension as X
        - each column of X is multiplied by the corresponding magnitude in mag

        """
        (X, y) = ds
        Xprime = X * mag

        return (Xprime, y)
   
    def plot_scatter(self, ax, X, X_train, X_test,  y_train, y_test, ds_cnt):
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5

        h = .02  # step size in the mesh

        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        # just plot the dataset first

        if ds_cnt == 0:
            ax.set_title("Input data")

        # Plot the training points
        _= ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=self.cm_bright,
                   edgecolors='k')
        # Plot the testing points
        _= ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=self.cm_bright, alpha=0.6,
                   edgecolors='k')
        _= ax.set_xlim(xx.min(), xx.max())
        _= ax.set_ylim(yy.min(), yy.max())
        #_= ax.set_xticks(())
        #_= ax.set_yticks(())

        _ = ax.set_xlabel("Feature 1")
        _ = ax.set_ylabel("Feature 2")

        return (xx, yy)
    
    def plot_countour(self, ax, Z, X_train, X_test, y_train, y_test, xx, yy, name, score, ds_cnt):
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        _= ax.contourf(xx, yy, Z, cmap=self.cm, alpha=.8)

        # Plot the training points
        _= ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=self.cm_bright,
                   edgecolors='k')
        # Plot the testing points
        _= ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=self.cm_bright,
                   edgecolors='k', alpha=0.6)

        _= ax.set_xlim(xx.min(), xx.max())
        _= ax.set_ylim(yy.min(), yy.max())
        #_= ax.set_xticks(())
        #_= ax.set_yticks(())

        _ = ax.set_xlabel("Feature 1")
        _ = ax.set_ylabel("Feature 2")

        if ds_cnt == 0:
            _= ax.set_title(name)
        _= ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')

    
    def plot_classifiers(self, names=None, classifiers=None, num_samples=100, scale=True, num_ds=1):
        if names is None and classifiers is None:
            names, classifiers = self.names, self.classifiers

        X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                                   random_state=1, n_clusters_per_class=1)
        rng = np.random.RandomState(2)
        X += 2 * rng.uniform(size=X.shape)
        linearly_separable = (X, y)

        moons_ds = make_moons(noise=0.3, random_state=0, n_samples=num_samples)

        datasets = [ moons_ds,
                    self.stretch_ds(moons_ds, np.array([10,1])),
                    make_circles(noise=0.2, factor=0.5, random_state=1, n_samples=num_samples),
                    linearly_separable
                    ]

        # Short version: limit classifiers and datasets to num_ds
        names, classifiers, datasets = [ a[:num_ds] for a in [names, classifiers, datasets] ]
        figure = plt.figure(figsize=(12,6))
        i = 1
        # iterate over datasets
        for ds_cnt, ds in enumerate(datasets):
            ax = plt.subplot(len(datasets), len(classifiers) + 1, i)

            # preprocess dataset, split into training and test part
            X, y = ds

            # CHEATING ALERT: scaling BEFORE train/test split so info from test leaks into train
            if scale:
                X = StandardScaler().fit_transform(X)

            X_train, X_test, y_train, y_test = \
                train_test_split(X, y, test_size=.4, random_state=42)

            xx, yy = self.plot_scatter(ax, X, X_train, X_test,  y_train, y_test, ds_cnt)
            i += 1

            # iterate over classifiers
            for name, clf in zip(names, classifiers):
                ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
                clf.fit(X_train, y_train)
                score = clf.score(X_test, y_test)

                # Plot the decision boundary. For that, we will assign a color to each
                # point in the mesh [x_min, x_max]x[y_min, y_max].
                if hasattr(clf, "decision_function"):
                    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
                else:
                    Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

                self.plot_countour(ax, Z, X_train, X_test, y_train, y_test, xx, yy, name, score, ds_cnt)
                i += 1

        plt.tight_layout()
        return (names, classifiers, datasets)


class TransformHelper():
    def __init__(self, **params):
        return

    def plot_odds(self):
        p = np.linspace(0,1, 1000)

        # Note: add epsilon to denominator to prevent division by 0
        eps = 1e-6
        odds = (p + eps)/(1-p + eps)
        log_odds = np.log( odds )

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5) )

        # Drop the first/last points b/c they are infinite
        _ = axes[0].hist( odds[1:-1], bins=30 )
        _ = axes[0].set_title("odds")

        # Drop the first/last points b/c they are infinite
        _ = axes[1].hist( np.log(odds)[1:-1], bins=30 )
        _ = axes[1].set_title("Log odds")
