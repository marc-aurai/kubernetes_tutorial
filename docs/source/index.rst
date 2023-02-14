.. Kubernetes Tutorial documentation master file, created by
   sphinx-quickstart on Tue Feb 14 10:30:22 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Kubernetes Tutorial's documentation!
===============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   main
   utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

This repository is made by Marc Blomvliet (Aurai), and is for learning purpose only.

In this tutorial you will learn how to create an Docker image of your fastAPI application.
This application includes the following:

Takes two questions as input
Returns a prediction whether the two questions are similar or not similar
Saves the raw user input data in your MongoDB database
Saves the predictions in your MongoDB database

The application uses my own pre-trained model (with the use of MLFlow), the model is not very accurate but this is not the purpose of this training, neither to bother you with training your own model.

Furthermore, you will be introduced to MongoDB to create your own FREE database.
Test your Docker image with Docker.
Create a Kubernetes cluster with the same Docker image.
The Kubernetes cluster contains the following:

Deployment
Load balancer
Auto scaler (Horizontal Pod Auto scaler)
After you created your Kubernetes cluster, you will perform a stress/load test on your API and therefore on your Kubernetes cluster.