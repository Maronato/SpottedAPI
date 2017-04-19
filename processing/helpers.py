import os

from datasets.models import Approved, Rejected
import numpy as np
import requests
import cPickle
import boto
from boto.s3.key import Key
from django.conf import settings


def get_data(approved=True, detail=False):
    """Get Data
    returns a numpy array of dicts containing spotteds as specified

    approved: approved or rejected spotteds
    detail: wether or not to return the detailed reject reason
    """

    if approved:
        data = Approved.objects.all()
    else:
        data = Rejected.objects.all()

    arr = np.empty(shape=(len(data)), dtype=dict)

    for n, i in enumerate(data):
        if approved:
            arr[n] = {'message': i[0], 'reason': 'approved', 'suggestion': i[1]}
        else:
            arr[n] = {'message': i[0], 'reason': 'rejected' if not detail else i[1], 'suggestion': i[2]}

    return arr


def rand_reindex(arr):
    """Random reindex
    randomly reindexes an array
    """

    rand = np.arange(len(arr))
    np.random.shuffle(rand)
    return arr[rand]


def merge_data(approved, rejected, ratio=1):
    """Merge data
    merges approved and rejected arrays using a ratio to size the approved ones
    also reindexes them
    """

    approved = rand_reindex(approved)
    approved = approved[:(round(len(rejected) * ratio))]
    return rand_reindex(np.append(approved, rejected))


def stop_words():
    response = requests.get("https://gist.githubusercontent.com/alopes/5358189/raw/2107d809cca6b83ce3d8e04dbd9463283025284f/stopwords.txt")
    return response.text.split()


def reload_classifier(class_type, detailed):
    """Reload Classifier
    Reloads a classifier looking for it locally and in S3

    if it does not find it, return None
    """
    custom_path = class_type + '_detailed' if detailed else ''

    CLASSIFIER_PATH = 'classifier_' + custom_path + '.pkl'

    # Try to find it locally
    if os.path.exists(CLASSIFIER_PATH):
        return cPickle.load(open(CLASSIFIER_PATH))

    # Try to find it on S3
    conn = boto.connect_s3(settings.S3_KEY, settings.S3_SECRET)
    bucket = conn.get_bucket(settings.S3_BUCKET)
    try:
        k = Key(bucket, CLASSIFIER_PATH)
        k.get_contents_to_filename(CLASSIFIER_PATH)
        return cPickle.load(open(CLASSIFIER_PATH))
    except:
        return None


def save_classifier(classifier, class_type, detailed):
    """Save Classifier
    Saves a classifier to memory so that it can be easily accessed later
    """

    custom_path = class_type + '_detailed' if detailed else ''

    CLASSIFIER_PATH = 'classifier_' + custom_path + '.pkl'

    with open(CLASSIFIER_PATH, 'wb') as f:
        cPickle.dump(classifier, f)

    with open(CLASSIFIER_PATH) as f:

        conn = boto.connect_s3(settings.S3_KEY, settings.S3_SECRET)
        bucket = conn.get_bucket(settings.S3_BUCKET)

        k = Key(bucket)
        k.key = CLASSIFIER_PATH
        k.set_contents_from_file(f)
