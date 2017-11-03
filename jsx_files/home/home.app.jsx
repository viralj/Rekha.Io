class App extends React.Component {
    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col s12 m12 l12">
                        <p>Hello World!!!</p>
                        <p>This is test file!</p>
                    </div>
                </div>
            </div>
        );
    }
}


ReactDOM.render(<App />, document.getElementById('home-app'));