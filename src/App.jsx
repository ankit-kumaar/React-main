import Header from './components/Header/Header.jsx';
//for named import {}is required whereas for default it is not required.jyjf
//44 onwards
import CoreConcepts from './components/CoreConcepts.jsx';
import Examples from './components/Examples.jsx';


function App() {

  return (
    <>
      <Header />
      <main>
        <CoreConcepts />
        <Examples />
      </main>
    </>
  );
}

export default App;
