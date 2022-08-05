# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=191)
    payload = models.TextField()
    attempts = models.PositiveIntegerField()
    reserved_at = models.PositiveIntegerField(blank=True, null=True)
    available_at = models.PositiveIntegerField()
    created_at = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'jobs'


class Migrations(models.Model):
    migration = models.CharField(max_length=191)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Modules(models.Model):
    module_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'modules'


class OauthAccessTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.BigIntegerField(blank=True, null=True)
    client_id = models.PositiveIntegerField()
    name = models.CharField(max_length=191, blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_access_tokens'


class OauthAuthCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.BigIntegerField()
    client_id = models.PositiveIntegerField()
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_auth_codes'


class OauthClients(models.Model):
    user_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=191)
    secret = models.CharField(max_length=100, blank=True, null=True)
    redirect = models.TextField()
    personal_access_client = models.IntegerField()
    password_client = models.IntegerField()
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_clients'


class OauthPersonalAccessClients(models.Model):
    client_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_personal_access_clients'


class OauthRefreshTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    access_token_id = models.CharField(max_length=100)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_refresh_tokens'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class PermissionRoles(models.Model):
    permission_id = models.IntegerField()
    role_id = models.IntegerField()
    task_id = models.IntegerField()
    project_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'permission_roles'


class Permissions(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    task_id = models.IntegerField()
    module_id = models.IntegerField()
    permission_type_status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'permissions'


class ProcoreAccessToken(models.Model):
    access_token = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'procore_access_token'


class SuperAdmins(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    country_code = models.CharField(max_length=50)
    mobile_no = models.BigIntegerField()
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'super_admins'


class SyncTables(models.Model):
    company_id = models.IntegerField()
    closeout_company_id = models.IntegerField()
    closeout_project_id = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField()
    response_id = models.CharField(max_length=2000, blank=True, null=True)
    issync = models.IntegerField(db_column='isSync')  # Field name made lowercase.
    sync_progress = models.IntegerField()
    syncby = models.IntegerField(db_column='syncBy', blank=True, null=True)  # Field name made lowercase.
    isautosync = models.IntegerField(db_column='isAutoSync')  # Field name made lowercase.
    issubmmitalsync = models.IntegerField(db_column='isSubmmitalSync', blank=True, null=True)  # Field name made lowercase.
    isprogressphotosync = models.IntegerField(db_column='isProgressPhotoSync')  # Field name made lowercase.
    sync_date_time = models.DateTimeField()
    sync_start_date_time = models.DateTimeField()
    access_token = models.TextField()
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    isdeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sync_tables'


class SyncTimeLogs(models.Model):
    project_id = models.IntegerField()
    sync_start_time = models.DateTimeField()
    sync_end_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sync_time_logs'


class TblApproveSubmittals(models.Model):
    procore_submittal_id = models.IntegerField()
    spec_section = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    sort_number = models.CharField(max_length=255, blank=True, null=True)
    n_revision = models.CharField(max_length=200)
    title = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=200)
    responsible_contractor = models.CharField(max_length=200, blank=True, null=True)
    project_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    status_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_approve_submittals'


class TblCloseoutItemType(models.Model):
    type_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_closeout_item_type'


class TblCloseoutItemUploads(models.Model):
    file = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=255)
    closeout_item_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_closeout_item_uploads'


class TblCloseoutItems(models.Model):
    item_name = models.CharField(max_length=255, blank=True, null=True)
    division_no = models.CharField(max_length=11, blank=True, null=True)
    spec_sec_no = models.CharField(max_length=255)
    spec_sec_description = models.CharField(max_length=255)
    submittal_no = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=255)
    created_by = models.IntegerField(blank=True, null=True)
    responsible_contractor_name = models.CharField(max_length=255)
    responsible_contractor_id = models.IntegerField()
    contact_person_email = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    remark = models.TextField()
    due_date = models.DateField()
    isdeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    project_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_closeout_items'


class TblCloseoutManual(models.Model):
    manual_link = models.CharField(max_length=255)
    version = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_closeout_manual'


class TblCompanies(models.Model):
    procore_company_id = models.IntegerField()
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.IntegerField(blank=True, null=True)
    mobile_no = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.
    is_registered = models.IntegerField()
    project_limit = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_companies'


class TblCompanyUsers(models.Model):
    user_id = models.IntegerField()
    company_id = models.IntegerField()
    role_id = models.IntegerField()
    isactive = models.IntegerField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    isprocoreuser = models.IntegerField(db_column='isProcoreUser')  # Field name made lowercase.
    ispasswordchange = models.IntegerField(db_column='isPasswordChange')  # Field name made lowercase.
    issuperadmin = models.IntegerField(db_column='isSuperAdmin')  # Field name made lowercase.
    isdeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_company_users'


class TblCoverPages(models.Model):
    project_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    pdf_path = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_cover_pages'


class TblCustomRoles(models.Model):
    role_id = models.IntegerField()
    company_id = models.IntegerField()
    project_id = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_custom_roles'


class TblDrawingSets(models.Model):
    project_id = models.IntegerField()
    procore_set_id = models.IntegerField()
    set_name = models.CharField(max_length=255)
    set_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_drawing_sets'


class TblDrawings(models.Model):
    procore_drawing_id = models.IntegerField()
    project_id = models.IntegerField()
    number = models.CharField(max_length=255)
    discipline = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    revision = models.IntegerField()
    drawing_set_id = models.IntegerField()
    trade_id = models.IntegerField()
    attachment = models.CharField(max_length=255)
    closeout_attachment = models.CharField(max_length=2000, blank=True, null=True)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    png_attachment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_drawings'


class TblIndexPages(models.Model):
    project_id = models.IntegerField()
    pdf_path = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_index_pages'


class TblMasterSectionList(models.Model):
    section_name = models.CharField(max_length=255)
    folder_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_master_section_list'


class TblProgressphotos(models.Model):
    procore_photo_id = models.IntegerField()
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=5)
    photo_date = models.DateField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_progressphotos'


class TblProjectAssigns(models.Model):
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    isdeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    role_id = models.IntegerField()
    isinvited = models.IntegerField(db_column='isInvited')  # Field name made lowercase.
    is_visible = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_project_assigns'


class TblProjectContacts(models.Model):
    project_id = models.IntegerField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    procore_id = models.IntegerField(blank=True, null=True)
    is_visible = models.IntegerField()
    status = models.IntegerField()
    role_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_project_contacts'


class TblProjectIndex(models.Model):
    project_id = models.IntegerField()
    section_id = models.IntegerField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_project_index'


class TblProjects(models.Model):
    procore_project_id = models.IntegerField()
    project_name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    ebinder_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    project_logo = models.CharField(max_length=255, blank=True, null=True)
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    project_status = models.IntegerField()
    reimport_status = models.IntegerField(blank=True, null=True)
    isdeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    company_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_projects'


class TblResponseFilters(models.Model):
    project_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    procore_response_id = models.IntegerField()
    response_value = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_response_filters'


class TblRfiAnswers(models.Model):
    procore_answer_id = models.IntegerField()
    rfi_id = models.IntegerField()
    answer = models.TextField()
    answer_date = models.DateTimeField()
    official = models.CharField(max_length=233)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_rfi_answers'


class TblRfiAttachments(models.Model):
    procore_attachment_id = models.BigIntegerField()
    answer_id = models.IntegerField()
    file_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    rfi_id = models.IntegerField(blank=True, null=True)
    closeout_attachment_url = models.CharField(max_length=2000, blank=True, null=True)
    closeout_rfi_attachments_url = models.CharField(max_length=255, blank=True, null=True)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_rfi_attachments'


class TblRfiQuestions(models.Model):
    procore_question_id = models.IntegerField()
    question_body = models.TextField()
    rfi_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    question_date = models.DateTimeField()
    created_by = models.CharField(max_length=255)
    project_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_rfi_questions'


class TblRfiQuestionsAttachments(models.Model):
    procore_attachment_id = models.BigIntegerField()
    question_id = models.IntegerField()
    file_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    rfi_id = models.IntegerField(blank=True, null=True)
    closeout_attachment_url = models.CharField(max_length=2000, blank=True, null=True)
    closeout_rfi_attachments_url = models.CharField(max_length=255, blank=True, null=True)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_rfi_questions_attachments'


class TblRfis(models.Model):
    procore_rfi_id = models.IntegerField()
    subject = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100)
    question_body = models.TextField()
    responsible_contractor = models.CharField(max_length=255, blank=True, null=True)
    assignees = models.CharField(max_length=255, blank=True, null=True)
    close_date = models.DateTimeField()
    due_date = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    received_from = models.CharField(max_length=255, blank=True, null=True)
    cost_code = models.CharField(max_length=255, blank=True, null=True)
    schedule_impact = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    project_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    date_initiated = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_rfis'


class TblRoles(models.Model):
    role_name = models.CharField(max_length=200)
    custom_role = models.IntegerField()
    is_company_role = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_roles'


class TblSpecSectionDivisions(models.Model):
    procore_division_id = models.IntegerField()
    project_id = models.IntegerField()
    description = models.CharField(max_length=255)
    number = models.CharField(max_length=100)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_spec_section_divisions'


class TblSpecSections(models.Model):
    procore_spec_sec_id = models.IntegerField()
    project_id = models.IntegerField()
    number = models.CharField(max_length=255)
    sort_number = models.CharField(max_length=11)
    description = models.CharField(max_length=255)
    revision = models.CharField(max_length=255)
    issued_date = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.CharField(max_length=2000, blank=True, null=True)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_spec_sections'


class TblSpecifications(models.Model):
    procore_spec_id = models.IntegerField()
    project_id = models.IntegerField()
    number = models.CharField(max_length=100)
    sort_number = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    revision = models.IntegerField(blank=True, null=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    spec_set = models.CharField(max_length=255, blank=True, null=True)
    spec_cat_id = models.IntegerField(blank=True, null=True)
    closeout_company_id = models.IntegerField(blank=True, null=True)
    current_revision_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_specifications'


class TblSubmittalAttachments(models.Model):
    submittal_id = models.IntegerField()
    submittal_attachment_id = models.BigIntegerField()
    attachment_name = models.CharField(max_length=255)
    attachment_url = models.CharField(max_length=255)
    closeout_attachment_url = models.CharField(max_length=2000, blank=True, null=True)
    filename = models.CharField(max_length=255)
    project_id = models.IntegerField()
    closeout_company_id = models.IntegerField(blank=True, null=True)
    submittal_workflow_id = models.IntegerField()
    procore_workflow_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_submittal_attachments'


class TblSubmittalStatusId(models.Model):
    submittal_id = models.IntegerField()
    submittal_status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_submittal_status_id'


class TblSubmittalWorkflow(models.Model):
    procore_workflow_id = models.IntegerField()
    procore_submittal_id = models.IntegerField()
    submittal_id = models.IntegerField()
    response_id = models.IntegerField()
    response = models.CharField(max_length=255)
    submittal_attachment_id = models.IntegerField()
    project_id = models.IntegerField()
    returned_date = models.DateField(blank=True, null=True)
    sent_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_submittal_workflow'


class TblTrades(models.Model):
    procore_drawing_discipline_id = models.IntegerField()
    position = models.IntegerField()
    name = models.CharField(max_length=255)
    project_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_trades'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
