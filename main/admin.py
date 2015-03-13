from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from main.models import *


# Register your models here.
class TurkUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'worker_id', 'condition', 'initial_browser_details', 'final_browser_details', 'start_time', 'finish_time')

	def user_id(self):
		return self.user.id


class TurkUserInline(admin.StackedInline):
	model = TurkUser
	can_delete = False
	verbose_name_plural = 'employee'

#class TurkAssignmentAdmin(admin.ModelAdmin):
#	list_display = ('id', 'assignment', 'hit', 'turksubmit', 'browser_details', 'condition', 'start_time', 'finish_time', )

class TweetAdmin(admin.ModelAdmin):
	list_display = ('id', 'text', 'screen_name',)


class CodeAdmin(admin.ModelAdmin):
	list_display = ('id', 'schema', 'name', 'description',)


class CodeInstanceAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'deleted', 'code', 'tweet', 'assignment',)




class UserAdmin(UserAdmin):
    inlines = (TurkUserInline, )
    list_display = ('id', 'username', 'email', 'turkuser_id', 'is_active', 'is_staff', 'is_superuser')

    def turkuser_id(self, obj):
    	return obj.turkuser.id if obj.turkuser is not None else None

#
# register admin handlers
#

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#admin.site.register(TurkUser,TurkUserAdmin)
#admin.site.register(TurkAssignment,TurkAssignmentAdmin)
admin.site.register(Tweet,TweetAdmin)
admin.site.register(Code,CodeAdmin)
admin.site.register(CodeInstance,CodeInstanceAdmin)

