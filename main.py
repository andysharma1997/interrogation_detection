from initializer import phrase_maker, get_doc
from flask import Flask, Response, request
import jsonpickle

matcher = phrase_maker()

app = Flask(__name__)


def interrogation_detector(sentence):
    """
    @author: andy
    :parameter sentence to be checked
    :returns The type of question and the if not a question it tells that also
    """
    ver_tags = ["VBZ", "VB", "VBD", "VBG", "VBN", "VBP"]
    doc = get_doc(sentence)
    matches = matcher(doc)
    if len(matches) != 0:
        first_filter = doc[matches[0][1]:]
        tag_list = [item.tag_ for item in first_filter]
        dep_list = [item.dep_ for item in first_filter]

        if "subj" in first_filter[0].dep_ or "obj" in first_filter[0].dep_:
            return {"question": str(first_filter), "subject": "will be in answer",
                    "tag": "direct-question without subject"}
        try:
            flag = False
            for i in range(1, len(tag_list)):
                for j in range(i + 1, len(tag_list)):
                    if tag_list[i] in ver_tags and "nsubj" in dep_list[j]:
                        print(j, dep_list[j])
                        flag = True
                        subject_index = j
                        break
            if flag:
                return {"question": str(first_filter), "subject": str(first_filter[subject_index]),
                        "tag": "direct-question"}
        except IndexError:
            pass
    elif doc[0].pos_ == "VERB" or doc[0].tag_ in ver_tags:
        if len(doc) > 3:
            if "neg" in doc[1].dep_:
                if doc[2].tag_ in ver_tags and "nsubj" not in [item.dep_ for item in doc]:
                    subject = []
                    objects = []
                    for tok in doc:
                        if "subj" in tok.dep_:
                            subject.append(str(tok))
                        if "obj" in tok.dep_:
                            objects.append(str(tok))
                    return {"question": str(sentence), "subject": subject, "object": objects,
                            "tag": "negation yes/no question"}
                if doc[2].tag_ in ver_tags and "nsubj" in [item.dep_ for item in doc]:
                    subject = []
                    objects = []
                    for tok in doc:
                        if "subj" in tok.dep_:
                            subject.append(str(tok))
                        if "obj" in tok.dep_:
                            objects.append(str(tok))
                    return {"question": str(sentence), "subject": str(doc[[item.dep_ for item in doc].index("nsubj")]),
                            "objects": objects, "tag": "negation yes/no question"}
            else:
                if ("nsubj" in doc[1].dep_) or ("DET" in doc[1].pos_ and "nsubj" in doc[2].dep_):
                    if "or" in [str(item) for item in doc]:
                        return {"question": str(sentence), "tag": "alternative interrogative"}
                    subject = []
                    objects = []
                    for tok in doc:
                        if "subj" in tok.dep_:
                            subject.append(str(tok))
                        if "obj" in tok.dep_:
                            objects.append(str(tok))
                    return {"question": str(sentence), "subject": subject, "objects": objects, "tag": "yes/no question"}
        else:
            return {'tag': "not a question"}
    else:
        return {'tag': "not a question"}


def check_question(sentence):
    resp = interrogation_detector(sentence)
    flag = False
    if resp is not None:
        if resp['tag'] != "not a question":
            flag = True
    return flag


@app.route('/get_interrogation_type', methods=["POST", "GET"])
def get_interrogation_type():
    sentence = request.args.get("sentence")
    print(sentence)
    result = interrogation_detector(sentence)
    print(result)
    if result is not None:
        resp = Response(jsonpickle.encode(result), mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = Response(jsonpickle.encode({'tag': "not a question"}), mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/get_interrogation', methods=["POST", "GET"])
def get_true_false():
    sentence = request.args.get("sentence")
    resp = Response(jsonpickle.encode(str(check_question(sentence))), mimetype='application/text')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(host='localhost', port=9999, debug=True)
