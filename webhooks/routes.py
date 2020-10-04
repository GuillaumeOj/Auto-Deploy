from flask import Response
from flask import abort
from flask import request

from webhooks import app
from webhooks.utils import NoSignature
from webhooks.utils import WrongDigestMode
from webhooks.utils import WrongSignatureType
from webhooks.utils import verify_signature


@app.route("/", methods=["GET", "POST"])
def landing():
    if request.method == "POST":

        try:
            if verify_signature(request):
                return Response("Everything is ok!", status=200)
        except NoSignature:
            abort(Response("The signature is missing", status=403))
        except WrongDigestMode:
            abort(Response("Only sha1 could be used", status=403))
        except WrongSignatureType:
            abort(
                Response("The given signature don't match the expected form", status=403)
            )
        else:
            abort(
                Response("The given signature don't match with the payload", status=403)
            )

    return "Nothing here..."
