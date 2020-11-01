from django.db import models

# Create your models here.

class SPManager (models.Manager):
    def __init__(self, SPName):
        self.name = SPName
        self.param_dict = {}

    def sql (self, param_dict_in): 
        self.param_dict.update(param_dict_in)
        print ('following are the key:values sent by client and accepted by the method')
        print (self.param_dict)

        from django.db import connection
        list_param_raw = []
        with connection.cursor() as cursor:
            cursor.execute ("SELECT PARAMETER_NAME FROM INFORMATION_SCHEMA.PARAMETERS WHERE SPECIFIC_NAME= %s and PARAMETER_MODE = 'IN' order by ORDINAL_POSITION asc",[self.name])
            for row in cursor.fetchall():
                list_param_raw.append(row[0])
            print ('following are sp parameters extracted from sql and containing @')
            print (list_param_raw)

            sql = 'exec {0} '.format(self.name)
            p = ''
            for param in list_param_raw:
                p = p + param + " = %s, "
            sql = sql + p[:-2]
            print ('following is constructed sql with placeholders')
            print (sql)

            param_key = [s.replace('@', '') for s in list_param_raw]
            print ('following are the keys')
            print (param_key)

            param_value = []
            for key in param_key:
                param_value.append(self.param_dict.get(key))
            print ('following parameters will be passed to the sp')
            print (param_value)

            cursor.execute(sql,param_value) #SP must have SET NOCOUNT ON just after 'Begin' statement

            print ('SP executed')

            self.param_dict.clear()
            list_param_raw.clear()
            param_key.clear()
            param_value.clear()            

            result_list = []
            try:
                keys = [col[0] for col in cursor.description]        
                for row in cursor.fetchall():
                    result_list.append(dict(zip(keys,row)))
            except:
                result_list = [{"Results":"No Results Returned"}]

            if len(result_list) == 0:
                result_list = [{"Results":"No Results Found"}]
        
        return result_list

class search_doctor_sp (models.Model):
    #row_no = models.IntegerField()
    #PatientUID = models.CharField(max_length=100)
    #Fname = models.CharField(max_length=25)
    #Lname = models.CharField(max_length=25)
    #Gender = models.CharField(max_length=10)
    #DOB = models.DateField()
    #Mob = models.CharField(max_length=25)
    #count = models.IntegerField()
    objects = SPManager('SearchDoctor')
    class Meta:
        managed = False #ensures that table is not created / modified by Django    

class doctor_details_by_username_sp (models.Model):
    objects = SPManager('GetProfileDataByUser')
    class Meta:
        managed = False

class add_bookings_sp (models.Model):
    objects = SPManager('InsertBookings')
    class Meta:
        managed = False

class Bookings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField()
    username = models.CharField(max_length=15)
    caller_fname = models.CharField(db_column='caller_Fname', max_length=25, blank=True, null=True)  # Field name made lowercase.
    caller_lname = models.CharField(db_column='caller_Lname', max_length=25, blank=True, null=True)  # Field name made lowercase.
    caller_mob = models.CharField(db_column='caller_Mob', max_length=15, blank=True, null=True)  # Field name made lowercase.
    book_date = models.DateField(db_column='Book_date', blank=True, null=True)  # Field name made lowercase.
    book_timeslot = models.TimeField(db_column='Book_timeslot', blank=True, null=True)  # Field name made lowercase.
    createddatetime = models.DateTimeField(db_column='createdDatetime', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(blank=True, null=True)
    patientid = models.IntegerField(db_column='PatientID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Bookings'