class App extends React.Component {

    createForm(){
        let form_fields = [];

        for(let i=0;i<RIAskQ.form.length;i++){
            console.log(RIAskQ.form[i]);
        }

    }

    render() {

        this.createForm();

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
                                        <span className="card-title">Item</span>
                                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                                            tempor incididunt ut labore et dolore magna aliqua.</p>
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


ReactDOM.render(<App />, document.getElementById('questions-ask-app'));