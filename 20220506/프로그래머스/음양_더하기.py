def solution(absolutes, signs):
    return sum(map(lambda a: a[1] if a[0] else -1*a[1] , zip( signs, absolutes)))
# https://programmers.co.kr/learn/courses/30/lessons/76501
