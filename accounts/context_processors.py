def employee_data(request):

    if request.user.is_authenticated:

        return {
            "employee": request.user.employee
        }

    return {}