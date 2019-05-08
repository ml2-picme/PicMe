import requests

# returns a words list, including parent and children words for a given synset-ID
def getWords(synsetId):
    result = getWordsBySynsetId(synsetId)
    if len(result) > 0:
        # get child IDs
        parentToChildren = getParentToChildrenDictionary()
        if synsetId in parentToChildren:
            children = getParentToChildrenDictionary()[synsetId]
        else:
            children = []
        # get words for child IDs
        print(('retrieving words for children: ' + str(children)))
        result.extend(getWordsBySynsetIds(children))

        # get parentd IDs
        childToParents = getChildToParentsDictionary()
        if synsetId in childToParents:
            parents = childToParents[synsetId]
        else:
            parents = []
        # get words for parent IDs
        print(('retrieving words for parents: ' + str(parents)))
        result.extend(getWordsBySynsetIds(parents))

    return result


# returns a words list from image-net for a given synset-ID
def getWordsBySynsetId(synsetId):
    # GET from image-net using curl
    url = "http://www.image-net.org/api/text/wordnet.synset.getwords?wnid=" + synsetId
    result = requests.get(url).text.split('\n')

    del result[-1]

    # in case of invalid id we get an 'invalid url' response
    if 'Invalid url!' in result:
        result = []

    print('Synset-ID ' + synsetId + ' has words ' + str(result))
    return result


# returns a words list from image-net for a list of synset-IDs
def getWordsBySynsetIds(synsetIdList):
    result = []
    if len(synsetIdList) > 0:
        for synsetId in synsetIdList:
            result.extend(getWordsBySynsetId(synsetId))
    return result


# returns a dictionary containing parent synset-IDs as keys and for each key a list of children synset ids
def getParentToChildrenDictionary():
    # GET from image-net using curl
    # response is a list where each item is of format 'parent child'
    wordnetHierachyList = requests.get("http://www.image-net.org/archive/wordnet.is_a.txt").text.split('\n')

    # check for invalid url response
    if 'The URL is not valid.' in wordnetHierachyList:
        return {}

    # transform list into dictionary
    d = {}

	#remove last object in list (empty)
    del wordnetHierachyList[-1]

    for item in wordnetHierachyList:
        parentChild = item.split(' ')
        parent = parentChild[0]
        child = parentChild[1]
        # is key (=parent) with value(=list of children) already defined?
        if parent in d:
            # add child to list
            list = d[parent]
            list.append(child)
        else:
            # create new list
            d[parent] = [child]
    return d


# returns a dictionary containing children synset-IDs as keys and for each key a list of parent synset ids
def getChildToParentsDictionary():
    # GET from image-net using curl
    # response is a list where each item is of format 'parent child'
    wordnetHierachyList = requests.get("http://www.image-net.org/archive/wordnet.is_a.txt").text.split('\n')

	#remove last object in list (empty)
    del wordnetHierachyList[-1]
	
    # check for invalid url response
    if 'The URL is not valid.' in wordnetHierachyList:
        return {}

    # transform list into dictionary
    d = {}
    for item in wordnetHierachyList:
        parentChild = item.split(' ')
        parent = parentChild[0]
        child = parentChild[1]
        # is key (=child) with value(=list of parents) already defined?
        if child in d:
            # add parent to list
            list = d[child]
            list.append(parent)
        else:
            # create new list
            d[child] = [parent]
    return d