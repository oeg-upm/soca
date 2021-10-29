import logo from './logo.svg';
import './App.css';
//import { BasicTable } from './components/BasicTable'
//import { FilteringTable } from './components/FilteringTable'
//import { PaginationTable } from './components/PaginationTable'
import { CatalogTable } from './components/CatalogTable'

function App() {
  return (
    <div className="App">
      <CatalogTable />
    </div>
  );
}

export default App;
