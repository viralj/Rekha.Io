class App extends React.Component {

    constructor() {
        super();
        this.createForm = this.createForm.bind(this);

    }

    createForm() {
        let form_fields = [];
        let csrf_token = document.getElementsByName('csrf_token');
        csrf_token = csrf_token[0].getAttribute('content');

        for (let i = 0; i < RIAskQ.form.length; i++) {
            let data_parent = "";
            let input_field = "";
            data_parent += Object.entries(RIAskQ.form[i].data.attrs.data_parent).map(([key, value]) => {
                return ` ${key}="${value.toString()}"`;
            });

            input_field += Object.entries(RIAskQ.form[i].data.input_field).map(([key, value]) => {
                if (value != null)
                    return ` ${key}="${value.toString()}"`;
            });

            form_fields.push(
                `<div class="row">
                    <div ${data_parent.toString()}>
                        <input ${input_field.toString()}/>
                        <label for="${RIAskQ.form[i].data.label}">${RIAskQ.form[i].data.label}</label>
                    </div>
                </div>`
            );

        }
        let form = `<form method="post" class="col s12" action="${RIAskQ.post}">${form_fields.toString().replace(new RegExp(",", 'g'), "")}</form>`;
        return (form)

    }

    render() {
        return (
            <div className="container">
                <div className="row"></div>
                <div className="row">
                    <div className="col s12 m12 l12">
                        <div className="row">
                            <div className="col s12 m3 l3 col-content right">
                                <div className="card">
                                    <div className="card-content">
                                        <span className="card-title">Item</span>
                                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                            tempor incididunt ut labore et dolore magna aliqua.</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col s12 m9 l9 col-content">
                                <div className="card">
                                    <div className="card-content">
                                        <span className="card-title">Ask question</span>
                                        {/*dangerouslySetInnerHTML={{html: this.props.createForm}}*/}
                                        <div className="col s12" dangerouslySetInnerHTML={{__html: this.createForm()}} />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


ReactDOM.render(<App/>, document.getElementById('questions-ask-app'));