from django.db import models
from users.models import CustomUser

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
                result_list = [{"Results":"API call is successful."}]

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

class add_appt_sp (models.Model):
    objects = SPManager('InsertComplaints')
    class Meta:
        managed = False

class DocDetail(models.Model):
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=15)
    doc_fname = models.CharField(db_column='doc_Fname', max_length=25)  # Field name made lowercase.
    doc_mname = models.CharField(db_column='doc_Mname', max_length=25, blank=True, null=True)  # Field name made lowercase.
    doc_lname = models.CharField(db_column='doc_Lname', max_length=25, blank=True, null=True)  # Field name made lowercase.
    doc_gender = models.CharField(db_column='doc_Gender', max_length=10, blank=True, null=True)  # Field name made lowercase.
    doc_dob = models.DateField(db_column='doc_DOB')  # Field name made lowercase.
    doc_graddegree = models.CharField(db_column='doc_GradDegree', max_length=10, blank=True, null=True)  # Field name made lowercase.
    doc_postgrad = models.CharField(db_column='doc_PostGrad', max_length=20, blank=True, null=True)  # Field name made lowercase.
    doc_phone = models.CharField(db_column='doc_Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    doc_email = models.CharField(db_column='doc_Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    clinic_address1 = models.CharField(max_length=100, blank=True, null=True)
    clinic_address2 = models.CharField(max_length=100, blank=True, null=True)
    clinic_city = models.CharField(max_length=25, blank=True, null=True)
    clinic_state = models.CharField(max_length=25, blank=True, null=True)
    clinic_pincode = models.CharField(max_length=10, blank=True, null=True)
    clinic_phone = models.CharField(max_length=20, blank=True, null=True)
    createddatetime = models.DateTimeField(db_column='createdDatetime', blank=True, null=True)  # Field name made lowercase.
    modifieddatetime = models.DateTimeField(db_column='modifiedDatetime', blank=True, null=True)  # Field name made lowercase.
    doc_services = models.CharField(db_column='doc_Services', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ispublish = models.BooleanField(blank=True, null=True)
    doc_clinicname = models.CharField(db_column='doc_Clinicname', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Doc_Detail'


class PatientDetail(models.Model):
    patientuid = models.CharField(db_column='PatientUID', primary_key=True, max_length=36)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=25)  # Field name made lowercase.
    mname = models.CharField(db_column='Mname', max_length=25, blank=True, null=True)  # Field name made lowercase.
    lname = models.CharField(db_column='Lname', max_length=25, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=10)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    mob = models.CharField(db_column='Mob', max_length=25, blank=True, null=True)  # Field name made lowercase.
    pemail = models.CharField(db_column='Pemail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pincode = models.CharField(max_length=25)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    occupation = models.CharField(max_length=25, blank=True, null=True)
    createddatetime = models.DateTimeField(db_column='createdDatetime', blank=True, null=True)  # Field name made lowercase.
    modifieddatetime = models.DateTimeField(db_column='modifiedDatetime', blank=True, null=True)  # Field name made lowercase.
    username_email = models.CharField(max_length=100, blank=True, null=True)
    userid = models.ForeignKey(DocDetail, null= True, on_delete=models.SET_NULL, db_constraint=False, db_column='userid')
    status = models.SmallIntegerField(blank=True, null=True, default=1)
    objects = models.Manager()
    add_pt_dr = SPManager('AddPatientDetail')

    class Meta:
        managed = False
        db_table = 'Patient_Detail'

class Appointments(models.Model):
    historyid = models.AutoField(primary_key=True)
    patientuid = models.ForeignKey(PatientDetail, null = True, on_delete=models.SET_NULL, db_constraint=False, db_column='PatientUID', max_length=36)  # Field name made lowercase.
    complaint = models.CharField(max_length=3000, blank=True, null=True)
    createddate = models.DateTimeField(db_column='createdDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='modifiedDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    patientcomplaint = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'complaints'