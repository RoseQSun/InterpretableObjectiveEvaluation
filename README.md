# Interpretable Objective Evaluation of Generative Models in Symbolic Music

## Description
This toolbox, ioeval, offers a reproducible and highly interpretable approach for evaluating the output of symbolic music generation models, especially in the context of deep learning, using a set of musicologically-informed objective metrics. 

## Novel Features
1. Proportion of rests on strong versus weak beats (ros/row)
2. Note duration on strong versus weak beats (los/low)
3. Scale degree on strong versus weak beats (sdos/sdow)
4. Average pitch interval in semitones (api)
5. Pitch range in semitones (pr)
6. Frequency of direction change (fdr)
7. Length of repeated groups in measures (lre)
8. Distance between repeated groups in measures (dbg)

## Distance Metrics
To identify which features are more discriminative, numerical features are input into a forward-stepwise logistic-regression model. This model identifies discriminative features by starting with the strongest predictor variable and proceeding through the remaining variables based on prediction strength.
Cross entropy for each feature is presented as a distance metric, calculated as the feature's log likelihood value divided by the number of observations in the model.

## Dependencies

 * [`numpy`](http://www.numpy.org)
 * [`music21`](https://github.com/cuthbertLab/music21)

## Install

clone branch and run

```sh
pip install -e .
```
