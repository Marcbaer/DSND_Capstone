'''This Script contains a function to evaluate implemented classifiers.'''

from sklearn.metrics import accuracy_score, f1_score

def evaluate_model(model,X,y):
    ''' 
    Function prints the accuracy and f1 score of a given classifier evaluated on input data.
    
    Input:
        model: trained classifier model
        X: Dataset containing features
        y: Dataset containing labels        
    Output:
        model_acc: Accuracy
        model_f1: F1 Score
        y: Dataset containing labels
    '''
    import re
    
    class_name = re.sub("[<>']", '', str(model.__class__))
    class_name = class_name.split(' ')[1]
    class_name = class_name.split('.')[-1]

    y_pred = model.predict(X)

    model_acc = accuracy_score(y, y_pred)
    model_f1 = f1_score(y, y_pred)
    
    print("%s model accuracy: %.3f" % (class_name, model_acc))
    print("%s model f1-score: %.3f" % (class_name, model_f1))    
    
    return model_acc, model_f1
    
