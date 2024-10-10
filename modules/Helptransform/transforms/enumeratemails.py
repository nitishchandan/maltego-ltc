from maltego_trx.entities import Email
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.Helptransform.extensions import Helptransform_registry, Helptransform_set

domains = [
    "@gmail.com", "@yahoo.com", "@outlook.com", "@icloud.com",
    "@aol.com", "@zoho.com", "@protonmail.com", "@proton.me",
    "@mail.com", "@yandex.com", "@gmx.com", "@fastmail.com",
    "@tutanota.com", "@me.com", "@hotmail.com"]

def generate_emails(username):
    email_list = []
    for domain in domains:
        email_list.append(f"{username}{domain}")
    return email_list
class enumeratemails(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        inputstr = request.Value
        username=inputstr.split("@")[0]
        emails = generate_emails(username)
        for email in emails:
            ent= response.addEntity("maltego.EmailAddress", email)

