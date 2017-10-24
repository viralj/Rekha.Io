/**
 * Created by Viral Joshi on 10/18/17.
 *
 * This is home js file which will contain all home page related frontend code for ReactJS.
 */

class App extends React.Component {
    render() {
        return (
            React.createElement("div", null, 
                React.createElement("p", null, "Hello World!!!"), 
                React.createElement("p", null, "This is test file!")
            )
        );
    }
}


ReactDOM.render(React.createElement(App, null), document.getElementById('home-app'));