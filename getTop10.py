import threading
import requests
import json
import heapq
import time  # 导入 time 模块，用于操作时间



# 获取查询参数
def get_parar(come, limit):
    payload = "[\r\n    {\r\n        \"operationName\": \"CuratedHomeFeedModuleQuery\",\r\n        \"variables\": {\r\n            \"paging\": {\r\n                \"from\": \"0\",\r\n                \"limit\": 25\r\n            }\r\n        },\r\n        \"query\": \"query CuratedHomeFeedModuleQuery($paging: PagingOptions!) {\\n  staffPicksFeed(input: {paging: $paging}) {\\n    items {\\n      ...CuratedHomeFeedItems_homeFeedItems\\n      __typename\\n    }\\n    pagingInfo {\\n      next {\\n        page\\n        limit\\n        from\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment CuratedHomeFeedItems_homeFeedItems on HomeFeedItem {\\n  __typename\\n  post {\\n    id\\n    title\\n    ...HomeFeedItem_post\\n    __typename\\n  }\\n}\\n\\nfragment HomeFeedItem_post on Post {\\n  __typename\\n  id\\n  title\\n  firstPublishedAt\\n  mediumUrl\\n  collection {\\n    id\\n    name\\n    domain\\n    logo {\\n      id\\n      __typename\\n    }\\n    __typename\\n  }\\n  creator {\\n    id\\n    name\\n    username\\n    imageId\\n    mediumMemberAt\\n    __typename\\n  }\\n  previewImage {\\n    id\\n    __typename\\n  }\\n  previewContent {\\n    subtitle\\n    __typename\\n  }\\n  readingTime\\n  tags {\\n    ...TopicPill_tag\\n    __typename\\n  }\\n  ...BookmarkButton_post\\n  ...OverflowMenuButtonWithNegativeSignal_post\\n  ...PostPresentationTracker_post\\n  ...PostPreviewAvatar_post\\n  ...Star_post\\n}\\n\\nfragment TopicPill_tag on Tag {\\n  __typename\\n  id\\n  displayTitle\\n  normalizedTagSlug\\n}\\n\\nfragment BookmarkButton_post on Post {\\n  visibility\\n  ...SusiClickable_post\\n  ...AddToCatalogBookmarkButton_post\\n  __typename\\n  id\\n}\\n\\nfragment SusiClickable_post on Post {\\n  id\\n  mediumUrl\\n  ...SusiContainer_post\\n  __typename\\n}\\n\\nfragment SusiContainer_post on Post {\\n  id\\n  __typename\\n}\\n\\nfragment AddToCatalogBookmarkButton_post on Post {\\n  ...AddToCatalogBase_post\\n  __typename\\n  id\\n}\\n\\nfragment AddToCatalogBase_post on Post {\\n  id\\n  isPublished\\n  __typename\\n}\\n\\nfragment OverflowMenuButtonWithNegativeSignal_post on Post {\\n  id\\n  visibility\\n  ...OverflowMenuWithNegativeSignal_post\\n  __typename\\n}\\n\\nfragment OverflowMenuWithNegativeSignal_post on Post {\\n  id\\n  creator {\\n    id\\n    __typename\\n  }\\n  collection {\\n    id\\n    __typename\\n  }\\n  ...OverflowMenuItemUndoClaps_post\\n  ...AddToCatalogBase_post\\n  __typename\\n}\\n\\nfragment OverflowMenuItemUndoClaps_post on Post {\\n  id\\n  clapCount\\n  ...ClapMutation_post\\n  __typename\\n}\\n\\nfragment ClapMutation_post on Post {\\n  __typename\\n  id\\n  clapCount\\n  ...MultiVoteCount_post\\n}\\n\\nfragment MultiVoteCount_post on Post {\\n  id\\n  __typename\\n}\\n\\nfragment PostPresentationTracker_post on Post {\\n  id\\n  visibility\\n  previewContent {\\n    isFullContent\\n    __typename\\n  }\\n  collection {\\n    id\\n    slug\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment PostPreviewAvatar_post on Post {\\n  __typename\\n  id\\n  collection {\\n    id\\n    name\\n    ...CollectionAvatar_collection\\n    __typename\\n  }\\n  creator {\\n    id\\n    username\\n    name\\n    ...UserAvatar_user\\n    ...userUrl_user\\n    ...useIsVerifiedBookAuthor_user\\n    __typename\\n  }\\n}\\n\\nfragment CollectionAvatar_collection on Collection {\\n  name\\n  avatar {\\n    id\\n    __typename\\n  }\\n  ...collectionUrl_collection\\n  __typename\\n  id\\n}\\n\\nfragment collectionUrl_collection on Collection {\\n  id\\n  domain\\n  slug\\n  __typename\\n}\\n\\nfragment UserAvatar_user on User {\\n  __typename\\n  id\\n  imageId\\n  mediumMemberAt\\n  membership {\\n    tier\\n    __typename\\n    id\\n  }\\n  name\\n  username\\n  ...userUrl_user\\n}\\n\\nfragment userUrl_user on User {\\n  __typename\\n  id\\n  customDomainState {\\n    live {\\n      domain\\n      __typename\\n    }\\n    __typename\\n  }\\n  hasSubdomain\\n  username\\n}\\n\\nfragment useIsVerifiedBookAuthor_user on User {\\n  verifications {\\n    isBookAuthor\\n    __typename\\n  }\\n  __typename\\n  id\\n}\\n\\nfragment Star_post on Post {\\n  id\\n  creator {\\n    id\\n    __typename\\n  }\\n  __typename\\n}\\n\"\r\n    }\r\n]"
    # payload = "[{\"operationName\":\"ClapCountQuery\",\"variables\":{\"postId\":\"971fab392751\"},\"query\":\"query ClapCountQuery($postId: ID!) {\\n  postResult(id: $postId) {\\n    __typename\\n    ... on Post {\\n      id\\n      clapCount\\n      __typename\\n    }\\n  }\\n}\\n\"},{\"operationName\":\"PostViewerEdgeQuery\",\"variables\":{\"postId\":\"971fab392751\"},\"query\":\"query PostViewerEdgeQuery($postId: ID!) {\\n  post(id: $postId) {\\n    ... on Post {\\n      id\\n      viewerEdge {\\n        __typename\\n        id\\n        clapCount\\n        readingList\\n        shareKey\\n        creatorPartnerProgramEnrollmentStatus\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"},{\"operationName\":\"CollectionViewerEdge\",\"variables\":{\"collectionId\":\"323c513f6364\"},\"query\":\"query CollectionViewerEdge($collectionId: IDu0021) {\\n  collection(id: $collectionId) {\\n    ... on Collection {\\n      id\\n      viewerEdge {\\n        ...Collection_viewerEdge\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment Collection_viewerEdge on CollectionViewerEdge {\\n  id\\n  canEditOwnPosts\\n  canEditPosts\\n  isEditor\\n  isFollowing\\n  isMuting\\n  isSubscribedToLetters\\n  isSubscribedToMediumNewsletter\\n  isSubscribedToEmails\\n  isWriter\\n  __typename\\n}\\n\"},{\"operationName\":\"UserViewerEdge\",\"variables\":{\"userId\":\"73e58dd22343\"},\"query\":\"query UserViewerEdge($userId: IDu0021) {\\n  user(id: $userId) {\\n    ... on User {\\n      id\\n      viewerEdge {\\n        ...User_viewerEdge\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment User_viewerEdge on UserViewerEdge {\\n  id\\n  createdAt\\n  hasCompletedProfile\\n  isAllowEdsEnabled\\n  isBlocking\\n  isFollowing\\n  isMuting\\n  isFacebookFollowing\\n  isMediumFollowing\\n  isSuperFollowing\\n  isTwitterFollowing\\n  isUser\\n  lastPostCreatedAt\\n  readPostsCount\\n  __typename\\n}\\n\"}]"
    payload_json = json.loads(payload)
    # 获取JSON字符串中的payload中的limit和from，并修改
    variables = payload_json[0]
    # 获取variables里的paging对象
    paging = variables['variables']['paging']
    #获取from和Limit对象
    paging['limit'] = limit
    paging['from'] = come
    print(payload_json)
    return payload_json

# 封装请求URL的函数
def requstmedium(url, payload):
    headers = {
        'authority': 'medium.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'apollographql-client-name': 'lite',
        'apollographql-client-version': 'main-20240105-143320-f2439d8bbc',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'g_state={"i_p":1704455237812,"i_l":1}; nonce=P3c1t73h; _gid=GA1.2.2112381953.1704448772; lightstep_guid/medium-web=f3b9693f8bde2f27; lightstep_session_id=f84398ff9f5599d8; sz=1857; pr=1; tz=-480; _ga=GA1.1.1497685297.1704448036; uid=lo_c6ef3fe43d07; sid=1:Qt7/wieRK466cilqWXaj/B7rIM0e4oHNdRtwsmyub6m/qHmh+VwP0Rq/2y8wTHAc; _ga_7JY7T788PK=GS1.1.1704455822.3.1.1704469220.0.0.0; _dd_s=rum=0&expire=1704470173023',
        'graphql-operation': 'CuratedHomeFeedModuleQuery',
        'medium-frontend-app': 'lite/main-20240105-143320-f2439d8bbc',
        'medium-frontend-path': '/?tag=software-engineering',
        'medium-frontend-route': 'homepage',
        'origin': 'https://medium.com',
        'ot-tracer-sampled': 'true',
        'ot-tracer-spanid': '2c3fa3c7175cdc43',
        'ot-tracer-traceid': '51880e7d77152859',
        'pragma': 'no-cache',
        'referer': 'https://medium.com/?tag=software-engineering',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }

    response = requests.request("POST", url, headers=headers, json=payload, timeout=10)
    # print(response.text)
    return response.text

# 定义一个线程函数
def request_thread(start, end,i):
    # 每个线程请求70次
    # 定义一个map，用于获取点赞数量前10的文章
    article_map = {}
    for i in range(start, end):
        #调用get_parar函数，获取请求头参数
        try:
            #定义from 和 limit 参数,并以字符串的方式传参
            f = str(i * 25)
            limit = str(25)
            parar = get_parar(f, limit)
            # 发送HTTP请求
            response = requstmedium('https://medium.com/_/graphql', parar)
            #调用requstmedium函数，获取返回值
            # 获取返回值中的data对象
            data = json.loads(response)[0]['data']
            # 获取data对象中的staffPicksFeed对象
            staffPicksFeed = data['staffPicksFeed']
            # 获取staffPicksFeed对象中的items对象
            items = staffPicksFeed['items']
            # results[i][0] += 1
            # success_count[i] += 1
            # 遍历items数组
            for item in items:
                # 获取item对象中的post对象
                post = item['post']
                # 获取post对象中的mediumUrl对象
                mediumUrl = post['mediumUrl']
                # 获取post对象中的clapCount
                clapCount = post['clapCount']
                # clapCount转成str，判断有没有K或者k，如果有，就转成int乘以1000
                # clapCount_str = str(clapCount)
                # if 'K' in clapCount_str:
                #     # 移除 'K'，转换为浮点数，然后乘以1000
                #     clapCount = int(float(clapCount_str.replace('K', '')) * 1000)
                # else:
                #     # 如果没有 'K'，直接转换为整数
                #     if 'k' in clapCount_str:
                #         clapCount = int(float(clapCount_str.replace('k', '')) * 1000)
                #     else:
                #         clapCount = int(clapCount)
                article_map[mediumUrl] = clapCount
        except Exception as e:
            print(f"An error occurred: {e}. Skipping this request.")
            # print(i, "执行第", i + 1, "次任务失败")
            # results[i][1] += 1
            # fail_count[i] += 1
            continue


    # print(article_map)
    # 从article_map利用小顶堆获取点赞数量前10的文章
    top10 = heapq.nlargest(10, article_map.items(), key=lambda x: x[1])
    print(top10)
    # 将top10中的数据追加到top10_articles中
    # 多线程访问top10_articles，需要加锁
    lock.acquire()
    for item in top10:
        top10_articles.append(item)
    lock.release()


# 创建一个堆来存储点赞数量前10的文章
top10_articles = []
# 创建一个锁对象
lock = threading.Lock()
# 创建50个线程
thread_num = 50
# 定义一个thread_num长度的数组，用于存储每个线程失败的次数
fail_count = [0] * thread_num
# 定义一个thread_num长度的数组，用于存储每个线程成功的次数
success_count = [0] * thread_num

def get_topsingle():
    t = threading.Thread(target=request_thread, args=(0, 1, 0))
    t.start()

def get_top10_all():
    # 一共要请求3480次，使用50个线程，每个线程请求70次
    mythreads = []
    # 记录失败次数
    f_count = 0
    # 记录成功的次数
    s_count = 0
    starttime = time.time()  # 记录开始时间 50

    for i in range(thread_num):
        # 计算每个线程的开始和结束位置
        # 定义每个线程循环步长
        step = 70
        start = i * step
        end = start + step
        t = threading.Thread(target=request_thread, args=(start, end, i))
        mythreads.append(t)
        t.start()

    # 等待所有线程完成

    for t in mythreads:
        t.join()
    # 计算成功次数
    # for i in range(thread_num):
    #     s_count += success_count[i]
    # 计算失败次数
    # for i in range(thread_num):
    #     f_count += fail_count[i]
    endtime = time.time()  # 记录结束时间
    minutes, seconds = divmod(endtime - starttime, 60)  # 记录结束时间
    # 打印耗时时分秒格式
    print("耗时: {}分{}秒".format(int(minutes), int(seconds)))
    # 合并所有线程的结果，得到最终的前10个

    final_top10 = heapq.nlargest(10, top10_articles, key=lambda item: item[1])
    for clapCount, url in final_top10:
        print(clapCount, url)
    # print(f"Total success requests: {s_count}")
    # print(f"Total failed requests: {f_count}")
    return final_top10, f_count*25



if __name__ == '__main__':
    get_top10_all();
    # get_topsingle();
