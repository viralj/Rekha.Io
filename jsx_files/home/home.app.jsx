/**
 * Created by Viral Joshi on 10/18/17.
 *
 * This is home js file which will contain all home page related frontend code for ReactJS.
 */

class App extends React.Component {
    render() {
        return (
            <div>
                <p>Hello World!!!</p>
                <p>This is test file!</p>
            </div>
        );
    }
}


ReactDOM.render(<App />, document.getElementById('home-app'));