from exts import db
from models import *
from datetime import datetime
import operator

def recommend(user_id):
    resource_list = []
    # for new user, recommend the resource that have most number of likes
    if Order.query.filter_by(consumer_id=user_id).all() is None or user_id==100:
        most_likes = Likes.query.order_by(Likes.num_likes.desc()).all()

        for resource in most_likes:
            result = Resource.query.filter_by(id=resource.id).first()
            resource_list.append(resource)
        return resource_list
    else:
        user_likes = User_resource_likes.query.filter_by(user_id=user_id).all()
        resource_dict = dict()
        #factor1: likes in common
        for each_like in user_likes:
            other_user = User_resource_likes.query.filter_by(likes=each_like.likes).all()
            for user in other_user:
                other_likes = User_resource_likes.query.filter_by(user_id=user.id).all()
                for resource in other_likes:
                    if Order.query.filter_by(consumer_id=user_id, resource_id=resource.id).all() is None:
                        if resource.id in resource_dict:
                            resource_dict[resource.id] += 1
                        else:
                            resource_dict[resource.id] = 1

        #factor2: fav list in common


        #factor3:type that have booked
        user_orders = Order.query.filter(consumer_id=user_id).all()
        for order in user_orders:
            type = Resource.query.filter_by(id=order.resource_id).with_entities(Resource.type).first()
            same_type_resource = Resource.query.filter_by(resource_type=type).all()
            for resource in same_type_resource:
                if Order.query.filter_by(consumer_id=user_id, resource_id=resource.id).all() is None:
                    if resource.id in resource_dict:
                        resource_dict[resource.id] += 1
                    else:
                        resource_dict[resource.id] = 1

        sorted_resource = dict(sorted(resource_dict.items(), key=operator.itemgetter(1), reverse=True))
        for key in sorted_resource:
            result = Resource.query.filter_by(id=sorted_resource[key]).first()
            resource_list.append(result)
        if len(resource_list) > 5:
            return resource_list[0:5]
        return resource_list
#recommendation algorithm
# def recommend(order, resource, wishlist, uid):
#     order = db.cursor()
#     resource = db.cursor()
#     wishlist = db.cursor()
#
#     resource.execute("Select recommend from user where user.id='" + uid + "'")
#     resource_list = resource.fetchall()
#
#     target_num = 5
#     if len(resource_list) < target_num:
#         target_num = len(resource_list)
#     num = 0
#
#     table_interest = find_interest(order, resource, wishlist, uid)
#     interest_type = table_interest[0]
#     interest_location = table_interest[1]
#
#     table_id = []
#     for i in range(len(interest_type)):
#         for j in range(len(resource_list)):
#             resource_id = resource_list[j][0]
#             resource_type = resource_list[j][2]
#             if interest_type[i] == resource_type:
#                 table_id.append(resource_id)
#                 num += 1
#                 if num == target_num:
#                     return table_id
#
#     for i in range(len(interest_location)):
#         for j in range(len(resource_list)):
#             resource_id = resource_list[j][0]
#             resource_location = resource_list[j][3]
#             if interest_location[i] == resource_location:
#                 table_id.append(resource_id)
#                 num += 1
#                 if num == target_num:
#                     return table_id
#
#     if num < target_num:
#         for i in range(len(resource_list)):
#             resource_id = resource_list[i][0]
#             table_id.append(resource_id)
#             num += 1
#             if num == target_num:
#                 return table_id
#
#     return table_id
#
#
# def add_type(table_type, resource_type):
#     if resource_type is None:
#         return table_type
#     type_num = len(table_type)
#     for i in range(type_num):
#         if table_type[i] == resource_type:
#             return table_type
#     table_type.append(resource_type)
#     return table_type
#
#
# def add_location(table_location, location):
#     if location is None:
#         return table_location
#     location_num = len(table_location)
#     for i in range(location_num):
#         if table_location[i] == location:
#             return table_location
#     table_location.append(location)
#     return table_location
#
#
# def find_resource(resource, resource_id):
#     empty = []
#     for i in range(len(resource)):
#         if resource[i][0] == resource_id:
#             return resource[i]
#     return empty
#
#
# def find_interest(order, resource, wishlist, uid):
#     order.execute("Select interest from user where userId='" + uid + "'")
#
#     table_type = []
#     table_location = []
#
#     order_list = order.fetchall()
#     order_num = len(order_list)
#
#     for i in range(order_num):
#         user_id = order_list[i][0]
#         resource_id = order_list[i][2]
#
#         if user_id == uid:
#             target_resource = find_resource(resource, resource_id)
#             table_type = add_type(table_type, target_resource[2])
#             table_location = add_location(table_location, target_resource[3])
#
#     wish_list = wishlist.fetchall()
#     wish_num = len(wish_list)
#
#     for i in range(wish_num):
#         user_id = wish_list[i][0]
#         resource_id = wish_list[i][1]
#
#         if user_id == uid:
#             target_resource = find_resource(resource, resource_id)
#             table_type = add_type(table_type, target_resource[2])
#             table_location = add_location(table_location, target_resource[3])
#
#     table_interest = [table_type, table_location]
#     return table_interest