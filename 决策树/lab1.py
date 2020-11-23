from math import log
import operator

def calcShannonEnt(dataSet):  # 计算数据的熵(entropy)
    numEntries=len(dataSet)  # 数据条数
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1] # 每行数据的最后一个字（类别）
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1  # 统计有多少个类以及每个类的数量
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries # 计算单个类的熵值
        shannonEnt-=prob*log(prob,2) # 累加每个类的熵值
    return shannonEnt

def createDataSet1():    # 创造示例数据
    dataSet = [
        # 1
        ['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.697, 0.460, '好瓜'],
        # 2
        ['乌黑', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', 0.774, 0.376, '好瓜'],
        # 3
        ['乌黑', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.634, 0.264, '好瓜'],
        # 4
        ['青绿', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', 0.608, 0.318, '好瓜'],
        # 5
        ['浅白', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.556, 0.215, '好瓜'],#######3
        # 6
        ['青绿', '稍蜷', '浊响', '清晰', '稍凹', '软粘', 0.403, 0.237, '好瓜'],
        # 7
        ['乌黑', '稍蜷', '浊响', '稍糊', '稍凹', '软粘', 0.481, 0.149, '好瓜'],
        # 8
        ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '硬滑', 0.437, 0.211, '好瓜'],
        # 9
        ['乌黑', '稍蜷', '沉闷', '稍糊', '稍凹', '硬滑', 0.666, 0.091, '坏瓜'],
        # 10
        ['青绿', '硬挺', '清脆', '清晰', '平坦', '软粘', 0.243, 0.267, '坏瓜'],
        # 11
        ['浅白', '硬挺', '清脆', '模糊', '平坦', '硬滑', 0.245, 0.057, '坏瓜'],##############
        # 12
        ['浅白', '蜷缩', '浊响', '模糊', '平坦', '软粘', 0.343, 0.099, '坏瓜'],###########
        # 13
        ['青绿', '稍蜷', '浊响', '稍糊', '凹陷', '硬滑', 0.639, 0.161, '坏瓜'],
        # 14
        ['浅白', '稍蜷', '沉闷', '稍糊', '凹陷', '硬滑', 0.657, 0.198, '坏瓜'],###########
        # 15
        ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '软粘', 0.360, 0.370, '坏瓜'],
        # 16
        ['浅白', '蜷缩', '浊响', '模糊', '平坦', '硬滑', 0.593, 0.042, '坏瓜'],###########3
        # 17
        ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑', 0.719, 0.103, '坏瓜']
    ]
    labels = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖率']#特征
    return dataSet,labels

def splitDataSet(dataSet,axis,value): # 按某个特征分类后的数据
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec =featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#MODIFY
def chooseBestFeatureToSplit(dataSet, labels):  # 选择最优的分类特征
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)  # 原始的熵
    bestInfoGain = 0.0
    bestFeature = -1

    #ADD2
    flagSeries = 0  # 是否为连续值
    bestSeriesMid = 0.0 # 若为连续值，记录最佳划分值

    #MODIFY
    # 对每个特征值求信息熵
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]

        if isinstance(featList[0], str): # 非连续值
            infoGain = calcInfoGain(dataSet, featList, i, baseEntropy)
        else: # 连续值
            infoGain, bestMid = calcInfoGainForSeries(dataSet, i, baseEntropy)

        # 信息增益更大，更新
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
            flagSeries = 0

            if not isinstance(dataSet[0][bestFeature], str):
                flagSeries = 1
                bestSeriesMid = bestMid

    if flagSeries:
        return bestFeature, bestSeriesMid
    else:
        return bestFeature

#ADD
# 计算非连续值信息增益
def calcInfoGain(dataSet, featList, i, baseEntropy):
    uniqueVals = set(featList)
    newEntropy = 0.0

    # 计算信息熵
    for value in uniqueVals:
        subDataSet = splitDataSet(dataSet, i, value)
        prob = len(subDataSet)/float(len(dataSet)) # 比例
        newEntropy += prob*calcShannonEnt(subDataSet)
    
    # 信息增益
    infoGain = baseEntropy - newEntropy
    return infoGain

#ADD
# 计算连续值信息增益
def calcInfoGainForSeries(dataSet, i, baseEntropy):
    maxInfoGain = 0.0 # 最大信息增益
    bestMid = -1 # 最佳分割点

    featList = [example[i] for example in dataSet]
    classList = [example[-1] for example in dataSet]
    dictList = dict(zip(featList, classList))

    # 将连续值从小到大排序
    sortedFeatList = sorted(dictList.items(), key=operator.itemgetter(0))
    numberForFeatList = len(dataSet) #连续值个数
    # 计算所有划分点
    midFeatList = [round((sortedFeatList[i][0] + sortedFeatList[i+1][0])/2.0, 3) for i in range(numberForFeatList-1)]

    # 计算每个划分点的信息增益
    for mid in midFeatList:
        # 将连续值按当前划分点划分为两部分
        eltDataSet, gtDataSet = splitDataSetForSeries(dataSet, i, mid)

        newEntropy = len(eltDataSet)/len(sortedFeatList)*calcShannonEnt(eltDataSet) + len(gtDataSet)/len(sortedFeatList)*calcShannonEnt(gtDataSet)
        # 信息增益
        infoGain = baseEntropy - newEntropy
        if infoGain > maxInfoGain:
            bestMid = mid
            maxInfoGain = infoGain

    return maxInfoGain, bestMid

#ADD
# 将连续值按当前划分点划分为两部分
def splitDataSetForSeries(dataSet, i, mid):
    eltDataSet = [] # <=mid的集合
    gtDataSet = [] # >mid的集合

    for feat in dataSet:
        if feat[i] <= mid:
            eltDataSet.append(feat)
        else:
            gtDataSet.append(feat)
    
    return eltDataSet, gtDataSet

def majorityCnt(classList):    #按分类后类别数量排序，比如：最后分类为2男1女，则判定为男；
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]  # 统计类别
    if classList.count(classList[0])==len(classList): # 只有一类
        return classList[0]
    if len(dataSet[0])==1:  # 只剩一列元素，分类结束
        return majorityCnt(classList)

    #MODIFY
    bestFeat=chooseBestFeatureToSplit(dataSet, labels) #选择最优特征的下标
    bestFeatLable = '' 
    flagSeries = 0 # 标记是否为连续值
    midSeries = 0.0 # 分界值

    if isinstance(bestFeat, tuple): # 结果为元组,是连续值
        bestFeatLable = str(labels[bestFeat[0]]) + '小于' + str(bestFeat[1]) + '?'
        midSeries = bestFeat[1]
        bestFeat = bestFeat[0]
        flagSeries = 1
    else:
        bestFeatLable = labels[bestFeat]
        flagSeries = 0

    myTree = {bestFeatLable: {}} # 最终决策树
    featValues = [example[bestFeat] for example in dataSet] # 当前特征的所有值

    if flagSeries:
        eltDataSet, gtDataSet = splitDataSetForSeries(dataSet, bestFeat, midSeries)
        subLables = labels[:]
        
        subTree = createTree(eltDataSet, subLables)
        myTree[bestFeatLable]['小于'] = subTree

        subTree = createTree(gtDataSet, subLables)
        myTree[bestFeatLable]['大于'] = subTree
        return myTree
    else:
        del (labels[bestFeat])
        uniqueVals = set(featValues)

        for value in uniqueVals:
            subLabels = labels[:]
            subTree = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
            myTree[bestFeatLable][value] = subTree
        return myTree



if __name__=='__main__':
    dataSet, labels=createDataSet1()  # 创造示列数据
    print(createTree(dataSet, labels))  # 输出决策树模型结果