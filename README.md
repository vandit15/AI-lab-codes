# AI-lab-codes
Scripts for the various Artificial Intelligence lab tasks


## LAB-3
The task is to perform [Part-of-Speech tagging](https://en.wikipedia.org/wiki/Part-of-speech_tagging) by building a [Hidden Markov Model](https://en.wikipedia.org/wiki/Hidden_Markov_model). the build model is dumped into pickle a file which is retrieved during testing

Dataset consists of words on different lines of a sentence which in turn are separeted by a blank line.

After building the model, [viterbi algorithm](https://en.wikipedia.org/wiki/Viterbi_algorithm) is applied to find the maximum probability tag for every word in the testing datset. The testing datset shoul consist of words that are in the model (smoothing hs not been performed on the model).


## LAB-4
The task is to perform Linear and Logistic regression on regression and classification datasets respectively. The model once built is dumped into pickle file.

For linear regression, learing rate is taken to be 0.001 with 200000 iterations.

For Logistic regression , learning rate is taken to be 0.015 with 60000 iterations.


