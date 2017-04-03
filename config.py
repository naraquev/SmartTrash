# ===== Your specific configuration goes below / please adapt ========

# the HCP account id - trial accounts typically look like p[0-9]*trial
hcp_account_id='i850231trial'

# you only need to adapt this part of the URL if you are NOT ON TRIAL but e.g. on PROD
hcp_landscape_host='.hanatrial.ondemand.com'
# hcp_landscape_host='.hana.ondemand.com' # this is used on PROD

# these credentials are used from applications with the "push messages to devices" API
hcp_user_credentials='User:Password'

# the following values need to be taken from the IoT Cockpit
device_id='7e921183-ff7e-499a-80f6-4177603232e0'
oauth_credentials_for_device='44651a87b9b4bfb124cde946a3fdb53'

message_type_id_isOn='207da5140d9a13273bdb'
message_type_id_Distance='a920dcd011ca1b4b0603'

# ===== nothing to be changed / configured below this line ===========
