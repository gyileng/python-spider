# -
每日代码
# 自己实现迭代器
# from collections import Iterable
# class Mylist(object):
#     def __init__(self, l):
#         self.l = l
#         self.num = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.num < len(self.l):
#             self.item = self.l[self.num]
#             self.num += 1
#             return self.item
#         else:
#             raise StopIteration
#
# if __name__ == '__main__':
#     mylist = Mylist([1,2,3,4,5,6,7,8])
#     for i in mylist:
#         print(i)

# 用迭代器实现斐波那契数列
# import time
# class Fib(object):
#     def __init__(self, num):
#         self.num = num
#         self.count = 0
#         self.num1 = 0
#         self.num2 = 1
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.count < self.num:
#             num = self.num1
#             self.num1, self.num2 = self.num2, self.num2 + self.num1
#             self.count += 1
#             time.sleep(1)
#             return num
#         else:
#             raise StopIteration
#
#
#
# if __name__ == '__main__':
#     fib = Fib(100)
#     for i in fib:
#         print(i)

# 用生成器实现斐波那契数列
# import time
# def Fib(num):
#     num = num
#     count = 0
#     num1, num2 = 0, 1
#     while count < num:
#         sum = num1
#         num1, num2 = num2, num1 + num2
#         count += 1
#         time.sleep(0.5)
#         yield sum
#
#
# if __name__ == '__main__':
#     fib = Fib(100)
#     for i in fib:
#         print(i)
