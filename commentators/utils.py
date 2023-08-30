import datetime

def mm_ss_to_seconds(mm_ss):
    mm_ss = mm_ss.split(':')
    minutes = int(mm_ss[0])
    seconds = int(mm_ss[1])
    return minutes * 60 + seconds