from crontab import CronTab

my_user_cron = CronTab(user=True)

job = my_user_cron.new(command='sudo /usr/bin/python3.5 /home/hyfgreg/updateData/test.py')

job.setall('*/1 * * * *')

job.enable()

my_user_cron.write()