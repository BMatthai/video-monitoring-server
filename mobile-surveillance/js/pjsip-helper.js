import {Endpoint} from 'react-native-pjsip'


export default class PjsipHelper extends Component {

	register() {
		console.log("registered ")

		// let endpoint = new Endpoint();
		// let state = await endpoint.start(); // List of available accounts and calls when RN context is started, could not be empty because Background service is working on Android
		// let {accounts, calls, settings, connectivity} = state;

		// // Subscribe to endpoint events
		// endpoint.on("registration_changed", (account) => {});
		// endpoint.on("connectivity_changed", (online) => {});
		// endpoint.on("call_received", (call) => {});
		// endpoint.on("call_changed", (call) => {});
		// endpoint.on("call_terminated", (call) => {});
		// endpoint.on("call_screen_locked", (call) => {}); // Android only
	}
}
