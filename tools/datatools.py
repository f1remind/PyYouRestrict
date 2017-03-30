def most_banned_tags(videos):
    minimum_amount = 10

    tags = {}
    # accumulate
    for video in videos:
        videotags = videos[video]['tags']
        for tag in videotags:
            restricted = videos[video]['restricted']
            if not tag in tags:
                tags[tag] = [0, 0]
            if restricted:
                tags[tag][1] += 1
            else:
                tags[tag][0] += 1
                
    #clean
    not_enough = []
    for tag in tags:
        if sum(tags[tag]) < minimum_amount: not_enough.append(tag)
    for tag in not_enough: tags.pop(tag)

    #synthesize
    taglist = []
    for tag in tags: taglist.append([
        tag,
        int(10000*tags[tag][1]/(tags[tag][1] + tags[tag][0]))/100,
        tags[tag][1] + tags[tag][0]
    ])

    #order
    taglist = sorted(taglist, key=lambda x: x[1])

    return taglist
