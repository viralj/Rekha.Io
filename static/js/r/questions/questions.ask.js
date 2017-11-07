class App extends React.Component {

    createForm() {
        let form_fields = [];
        let csrf_token = document.getElementsByName('csrf_token');
        csrf_token = csrf_token.getAttribute('content');
        alert(csrf_token);

        for (let i = 0; i < RIAskQ.form.length; i++) {
            let data_parent = "";
            let input_field = "";
            data_parent += Object.entries(RIAskQ.form[i].data.attrs.data_parent).map(([key, value]) => {
                return ` ${key}="${value.toString()}"`;
            });

            input_field += Object.entries(RIAskQ.form[i].data.input_field).map(([key, value]) => {
                if(value != null)
                    return ` ${key}="${value.toString()}"`;
            });

            form_fields.push(
                `<div className="row">
                    <div ${data_parent.toString()}>
                        <input ${input_field.toString()}/>
                        <label for="${RIAskQ.form[i].data.label}">${RIAskQ.form[i].data.label}</label>
                    </div>
                </div>`
            );

        }
        let form = `<form method="post" action="${RIAskQ.post}">${form_fields.toString()}</form>`;
        return(React.createElement("div", null, "this"))

    }

    render() {

        console.log(this.createForm());

        return (
            React.createElement("div", {className: "container"}, 
                React.createElement("div", {className: "row"}), 
                React.createElement("div", {className: "row"}, 
                    React.createElement("div", {className: "col s12 m12 l12"}, 
                        React.createElement("div", {className: "row"}, 
                            React.createElement("div", {className: "col s12 m3 l3 col-content right"}, 
                                React.createElement("div", {className: "card"}, 
                                    React.createElement("div", {className: "card-content"}, 
                                        React.createElement("span", {className: "card-title"}, "Item"), 
                                        React.createElement("p", null, "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod" + ' ' +
                                            "tempor incididunt ut labore et dolore magna aliqua.")
                                    )
                                )
                            ), 
                            React.createElement("div", {className: "col s12 m9 l9 col-content"}, 
                                React.createElement("div", {className: "card"}, 
                                    React.createElement("div", {className: "card-content"}, 
                                        React.createElement("span", {className: "card-title"}, "Item"), 
                                        React.createElement("p", null, "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod" + ' ' +
                                            "tempor incididunt ut labore et dolore magna aliqua.")
                                    )
                                )
                            )
                        )
                    )
                )
            )
        );
    }
}


ReactDOM.render(React.createElement(App, null), document.getElementById('questions-ask-app'));