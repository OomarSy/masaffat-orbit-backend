from packaging import version

from apps.appversion.models import AndroidAppRelease


class AppUpdateService:
    """
    service to check for app updates
    """

    @staticmethod
    def check_update(current_version: str, request=None):
        latest_version_obj = AndroidAppRelease.objects.filter(is_active=True).order_by('-created_at').first()

        if not latest_version_obj:
            return {
                "update_type": "none"
            }

        latest_ver = latest_version_obj.version
        minimum_ver = latest_version_obj.minimum_supported_version

        current_v = version.parse(current_version)
        latest_v = version.parse(latest_ver)
        minimum_v = version.parse(minimum_ver)

        if current_v < minimum_v:
            update_type = "force"
        elif current_v < latest_v:
            update_type = "optional"
        else:
            update_type = "none"

        result = {
            "update_type": update_type,
        }

        if update_type != "none" and latest_version_obj.apk_file:
            if request:
                result["apk_file_url"] = request.build_absolute_uri(latest_version_obj.apk_file.url)
            else:
                result["apk_file_url"] = latest_version_obj.apk_file.url  # fallback

        return result
