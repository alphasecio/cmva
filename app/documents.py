DOCUMENTS = {
    "1": {"owner_id": 100, "title": "Alice's report", "shared_with": []},
    "2": {"owner_id": 200, "title": "Bob's report", "shared_with": [300]},
}


def can_read(user_id, document):
    return user_id == document["owner_id"] or user_id in document["shared_with"]


def can_share(user_id, document):
    return user_id == document["owner_id"]


def get_document(document_id, user_id):
    document = DOCUMENTS.get(document_id)
    if document and can_read(user_id, document):
        return document
    return None


def share_document(document_id, user_id, target_user):
    document = DOCUMENTS.get(document_id)
    if not document:
        return False
    if can_read(user_id, document):
        document["shared_with"].append(target_user)
        return True
    return False
