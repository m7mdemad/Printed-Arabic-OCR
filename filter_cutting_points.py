import cv2
from scipy import stats
import numpy as np
import skimage.graph


def get_path_cost(skeleton, img, mti, s, t):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] == 255:
                skeleton[i,j] = True
            else:
                skeleton[i,j] = False
    array = np.asarray(skeleton)
    costs = np.where(array, 0.1,1000000000000000000 )
    path, cost = skimage.graph.route_through_array(
        costs, start=(mti, s -1), end=(mti, t), fully_connected=True)

    return cost


def horizintal_projection(im):
    #im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    projection = np.sum(im, 1)  # Calculate horizontal projection
    return projection

def vertical_projection(im):
    projection = np.sum(im, 0)
    return projection


def get_heighest_pixel_index(hp):
    i = 0
    while i < len(hp):
        if hp[i] != 0:
            break
        i += 1
    return i


def holeExist(word,boundaries, mti):
    img = word[0:mti, 0:word.shape[1]]
    vp_img = vertical_projection(img)

    for i in range(boundaries[1],boundaries[0]):
        if vp_img[i] == 0:
            return False
    return True


def baselineExist(word, boundaries, bl):
    count = 0
    for i in range(boundaries[1],boundaries[3]):
        if word[bl, i] == 0:
            count += 1
            # return False
    if count > 3:
        return False
    return True

def get_SHP(word, boundaries, start, end):
    img = word[start:end, boundaries[1]:boundaries[0]]
    # cv2.imwrite('zmzm.png', img)
    hp_img = horizintal_projection(img)
    return np.sum(hp_img)

def get_highest_left_pixel(word, boundaries1, boundaries2):
    img = word[0:word.shape[0], boundaries2[3]:boundaries1[3]]
    # cv2.imwrite('zgzag.png', img)
    vp_img = vertical_projection(img)

    i = 0
    while vp_img[i] == 0:
        i += 1

    j = 0
    while j < word.shape[0]:
        if img[j, i] != 0:
            return j
        j += 1

    return word.shape[0]


def components_count(img, bl):
    count = 0
    flag = 0
    for j in range(img.shape[1]):
        if img[bl, j] == 255 and flag == 0:
            count += 1
            flag = 1
        elif img[bl, j] != 255 and flag == 1:
            flag = 0

    return count



def get_stroke_cropping_indeces(hp, bl):
    start = 0
    i = bl
    while i >= 0:
        if hp[i] == 0 and i != bl:
            start = i
            break
        i -= 1

    end = len(hp) - 1
    i = bl
    while i <len(hp):
        if hp[i] == 0:
            end = i
            break
        i += 1
    return start, end

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

# check stroke conditions according to the paper
# get baseLine
def isStroke(word, boundaries1, boundaries2, bl, top_pixel_in_word_index, mfv, mfv1, mti, second):
    img = word[0:word.shape[0], boundaries1[3]:boundaries2[3]]
    start, end = get_stroke_cropping_indeces(horizintal_projection(img), bl)
    img1 = word[start:end, boundaries1[3]:boundaries2[3]]
    print(start, end)
    # word[bl, 0:word.shape[1]] = 255
    cv2.imwrite('zfttttt.png', img1)


    # cond1: single component
    if components_count(img, int(word.shape[0]/2)) > 1:
        print('cond1 checked')
        return False

    # cond2: SHPA > SHPB
    if get_SHP(img,[img.shape[1], 0], 0, bl) <= get_SHP(img, [img.shape[1], 0], bl, img.shape[0]):
        print('cond2 checked')
        return False

    # cond3: height of the seg is < 2*second peak of hp
    hp_img = horizintal_projection(img1)
    height_of_seg = bl - start
    # print('height_of_seg = ', height_of_seg)
    # todo: get real second peak
    # img1 = word[top_pixel_in_word_index + 2:word.shape[0], 0:word.shape[1]]
    second_peak = bl - second
    print('for cond3: ', height_of_seg, second_peak, img.shape[0])
    print('for cond3: ', img.shape[0] - height_of_seg, img.shape[0] - second_peak)
    if height_of_seg > second_peak:
        print('cond3 checked')
        cv2.imwrite('zfttttt.png', img1)

        return False

    # cond4: mode of vp(img) == MFV
    # I think paper wrote wrong condition
    hp_img = horizintal_projection(img1)
    hp_img = remove_values_from_list(hp_img, 0)
    m = stats.mode(hp_img)
    mode_hp = m[0][0]
    # print(mode_hp, mfv)
    if mfv == 0:
        mfv = mfv1
    if mode_hp not in range(mfv - 600, mfv + 600):
    #     print('cond4 checked',mode_hp, mfv,hp_img)
        # p = remove_values_from_list(hp_img, 0)
        # n = stats.mode(p)
        # mfv1 = n[0][0]
        print('cond4 checked', mode_hp, mfv)
        return False

    # cond5:
    if holeExist(img, [img.shape[1], 0], mti) or  holeExist(word, boundaries1, mti):
        print('cond5 checked')
        return False
    cv2.imwrite('zfttt.png', img1)
    # print(horizintal_projection(img1), mfv)
    return True


def dotsExist(word, boundaries1, boundaries2):
    img = word[0:word.shape[0], boundaries1[3]:boundaries2[3]]
    hp_img = horizintal_projection(img)

    count = 0
    flag = 0
    for j in range(len(hp_img)):
        if hp_img[j] > 0 and flag == 0:
            count += 1
            flag = 1
        elif hp_img[j] == 0 and flag == 1:
            flag = 0

    if count > 1:
        return True
    return False


def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]



def filter_cutting_points(skeleton, word, sr, baseLine, maxTransitionIndex, most_frequent_value, most_frequent_value_after_0, vp, hp, second):
    # print(vp, word.shape[1])
    i = 0
    valid_sr=[]
    top_pixel_in_word_index = get_heighest_pixel_index(hp)
    sr.reverse()

    # valid_sr.append(sr[0])
    while i < len(sr) - 1:
        cost = get_path_cost(skeleton, word, maxTransitionIndex, sr[i][1], sr[i][0])
        # print(path)

        # if i == 5:
        #     print('max index = ', word.shape[0] - top_pixel_in_word_index)
        #     print('left most = ', word.shape[0] - get_highest_left_pixel(word, sr[i], sr[i + 1]))
        #     print('baseline = ', word.shape[0] - baseLine)
            # mg = word[0:word.shape[0], sr[i+1][3]:sr[i][3]]
            # cv2.imwrite('zzzz.png', mg)

        # general case
        if vp[sr[i][3]] == 0:
            valid_sr.append(sr[i])
            i += 1

        # if no path exist
        elif cost > 1000000000000000000:
            print('path not detected', cost, i)
            valid_sr.append(sr[i])
            i += 1

        # detect holes case like: "ص, ض, ف, ه, ط"
        elif holeExist(word,sr[i],maxTransitionIndex):
            print('hole detected ', i)
            i += 1

        elif not baselineExist(word, sr[i], baseLine):
            print('no baseline', i, vp[sr[i][3]]/255, most_frequent_value, top_pixel_in_word_index)
            # handle cases of letters having curves like: "ص, ض, ن, س"
            # first one is SHPB and the second is SHPA
            if get_SHP(word, sr[i], baseLine, word.shape[0]) > get_SHP(word, sr[i], 0, baseLine):
                print('curve detected ',i)
                i += 1

            elif vp[sr[i][3]]/255 < most_frequent_value/255:
                # print( vp[sr[i][3]], most_frequent_value)
                valid_sr.append(sr[i])
                i += 1
            else:
                print(most_frequent_value,  vp[sr[i][3]])
                i += 1


        # might need to change operator
        elif (vp[sr[i + 1][3]] == 0 or i == len(sr) - 2) and (-get_highest_left_pixel(word, sr[i],sr[i + 1]) + baseLine) < int((-top_pixel_in_word_index + baseLine)/2):
            print(most_frequent_value/255, vp[sr[i][3]]/255, 'skip1', i, word.shape[0] - get_highest_left_pixel(word, sr[i],sr[i + 1]), word.shape[0] - top_pixel_in_word_index,word.shape[0] - baseLine)
            i += 1


        elif i < len(sr) - 1 and not isStroke(word, sr[i + 1], sr[i], baseLine, top_pixel_in_word_index, most_frequent_value, most_frequent_value_after_0, maxTransitionIndex, second):
            print('not stroke', i)
            if not baselineExist(word, sr[i + 1], baseLine) and vp[sr[i + 1][3]] < most_frequent_value:
                print('not stroke, dont add it', i, baselineExist(word, sr[i + 1], baseLine), vp[sr[i + 1][3]], most_frequent_value)
                i += 1
            else:
                print('not stroke, add it', i)
                valid_sr.append(sr[i])
                i += 1

        elif i < len(sr) - 1 and isStroke(word, sr[i + 1], sr[i], baseLine, top_pixel_in_word_index, most_frequent_value,
                            most_frequent_value_after_0, maxTransitionIndex, second) and dotsExist(word, sr[i + 1], sr[i]):
            print('is a stroke with dots', i)
            valid_sr.append(sr[i])
            i += 1

        elif i < len(sr) - 1 and isStroke(word, sr[i + 1], sr[i], baseLine, top_pixel_in_word_index, most_frequent_value,
                            most_frequent_value_after_0, maxTransitionIndex, second) and not dotsExist(word, sr[i + 1], sr[i]):
            print('seen case', i)
            if i < len(sr) - 2 and isStroke(word, sr[i + 2], sr[i + 1], baseLine, top_pixel_in_word_index, most_frequent_value,
                            most_frequent_value_after_0, maxTransitionIndex, second) and not dotsExist(word, sr[i + 2], sr[i + 1]):
                print('add seen 1', i)
                valid_sr.append(sr[i])
                i += 3
            elif i < len(sr) - 3 and isStroke(word, sr[i + 2], sr[i + 1], baseLine, top_pixel_in_word_index, most_frequent_value,
                            most_frequent_value_after_0, maxTransitionIndex, second) and dotsExist(word, sr[i + 2], sr[i + 1])and isStroke(word, sr[i + 3], sr[i + 2], baseLine, top_pixel_in_word_index, most_frequent_value,
                            most_frequent_value_after_0, maxTransitionIndex, second) and not dotsExist(word, sr[i + 3], sr[i + 2]):
                print('add seen 2', i)
                valid_sr.append(sr[i])
                i += 3

            else:
                i += 1

        else:
            print('none of them')
            valid_sr.append(sr[i])
            i += 1

    word[maxTransitionIndex, 0:word.shape[1]] = 255
    word[baseLine, 0:word.shape[1]] = 255
    for i in range(len(valid_sr )):
        word[0:word.shape[0], valid_sr[i][3]] = 255

    cv2.imwrite('zoo.png', word)


    return second, valid_sr