import logo from './logo.svg';
import './App.css';
//import { BasicTable } from './components/BasicTable'
import { FilteringTable } from './components/FilteringTable'
//import { PaginationTable } from './components/PaginationTable'

function App() {
  return (
    <div className="App">
      <FilteringTable />
    </div>
  );
}

export default App;
