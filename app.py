from flask import Flask, render_template,  request, jsonify

import model
import lstm
app = Flask(__name__)

@app.route("/model", methods=['POST','GET'])
def modeloutput():
    ans=("hi,hey,hello")
    if request.method == "POST":
        qtc_data = request.get_json()
        sentence =qtc_data[0]['sentence']
        
        if(sentence[len(sentence)-1]!= ' '):
            lis = list(sentence.split(" "))
            word =lis[len(lis)-1]
            ans = model.spellchecker.check(word)
        else:
            sentence = sentence.strip()
            ans = lstm.predict(sentence)
    print(ans)
    results = {'first': ans[0],'second': ans[1],'third':ans[2]}
    
    return jsonify(results)

@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)