# 移除记录相同的字段
def remove_duplicates(categories):
    # 将字典转换为元组并添加到集合中进行去重
    unique_categories = set(tuple(d.items()) for d in categories)

    # 将去重后的元组转换回字典，并组成列表
    unique_categories_list = [dict(t) for t in unique_categories]

    return unique_categories_list


# 移除字段相同的记录
def remove_duplicates_by_field(categories, field):
    unique_dict = {}
    for item in categories:
        field_value = item[field]
        if field_value not in unique_dict:
            unique_dict[field_value] = item

    unique_categories = list(unique_dict.values())
    return unique_categories


# 以json格式封装从数据库中返回的记录
def get_json_data(records):
    result = {"categories": [], "data": [], "links": []}
    name_dict = {}
    count = 0
    entity_temp = []
    categories_temp = []
    categories = []
    # 进行实体的去重
    for record in records:
        entity_temp.append(record['p.name'] + "_" + record['labels(p)'][0])
        entity_temp.append(record['n.name'] + "_" + record['labels(n)'][0])

        categories_temp.append(record['labels(p)'][0])
        categories_temp.append(record['labels(n)'][0])
    entity_temp = list(set(entity_temp))
    categories_temp = list(set(categories_temp))

    # 构建result中的data字段
    for data in entity_temp:
        splits = data.split("_")
        name_dict[splits[0]] = name_dict.get(splits[0], count)
        count += 1

        try:
            data_item = {'id': name_dict.get(splits[0]), 'name': splits[0],
                         'category': categories_temp.index(splits[1])}
            result['data'].append(data_item)
        except Exception as e:
            print(e)
            continue

    for category in categories_temp:
        if category == "Check":
            category = "检查"
        elif category == "Department":
            category = "所属科室"
        elif category == "Drug":
            category = "药物"
        elif category == "Disease":
            category = "疾病"
        elif category == "Symptom":
            category = "症状"
        elif category == "Food":
            category = "食品"
        elif category == "Producer":
            category = "药物成分"
        categories.append({"name": category})

    result['categories'] = categories

    # 构建resul中的links字段
    for record in records:
        try:
            link_item = {'source': name_dict.get(record['p.name']), 'target': name_dict.get(record['n.name']),
                         'value': record['r.name']}
            result['links'].append(link_item)
        except Exception as e:
            print(e)
            continue

    return result
