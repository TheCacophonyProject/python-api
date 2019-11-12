print('hello')
from  cacophonyapi.test.test_client_user_without_server  import Mocked_cacophonyapi  as mCS
from  cacophonyapi.test.notest_client_user_with_server  import  liveTESTcacophonyapi as mlCS

from requests_toolbelt import MultipartEncoder
import os
import json


mcs = mCS()
mlcs = mlCS()


mlcs.setUp()
mlcs.test_upload_recording()


mcs.setUp()

# mcs.test_version()
# with open(os.path.join("python-api","CODEOWNERS"),"rb") as f:
#     dir(f)
#     props = {"type": "thermalRaw"}
#     multipart_data = MultipartEncoder(
#     fields={"file": ("file.dat", f), "data": json.dumps(props)}
#         )


mcs.test_valid_upload_recording()