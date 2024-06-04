import { useState } from 'react';
import Header from './components/Header/Header.jsx';
//import componentsImg from './assets/components.png'
import { CORE_CONCEPTS } from './data.js';
import CoreConcept from './components/CoreConcept.jsx';
//for named import {}is required whereas for default it is not required.
import TabButton from './components/TabButton.jsx';
import { EXAMPLES } from './data.js';

function App() {
  const [ selectedTopic, setSelectedTopic ] = useState();

  function handleSelect(selectedButton){
    // selectedButton => 'components', 'jsx', 'props', 'state'
    setSelectedTopic(selectedButton);
    console.log(selectedTopic);
  }

  return (
    <div>
      <Header />
      <main>
        <section id="core-concepts">
          <h2>Core Concepts</h2>
          <ul>
            <CoreConcept 
             title={CORE_CONCEPTS[0].title}
             description={CORE_CONCEPTS[0].description}
             image={CORE_CONCEPTS[0].image}
            />
            <CoreConcept
            {...CORE_CONCEPTS[1]}  
             />
            <CoreConcept 
            {...CORE_CONCEPTS[2]}
            />
            <CoreConcept
            {...CORE_CONCEPTS[3]}
            />
          </ul>
        </section>
        <section id="examples">
          <h2>Examples</h2>
          <menu>
           <TabButton onSelect={() => handleSelect('components')}>
            Components
            </TabButton>
           <TabButton onSelect={() => handleSelect('jsx')}>JSX</TabButton>
           <TabButton onSelect={() => handleSelect('props')}>Props</TabButton>
           <TabButton onSelect={() => handleSelect('state')}>State</TabButton>
          </menu>
          { !selectedTopic && <p>Please select a topic.</p>}
          {selectedTopic && (
          <div id="tab-content">            
            <h3>{EXAMPLES[selectedTopic].title}</h3>
            <p>{EXAMPLES[selectedTopic].description}</p>
            <pre>
              <code>
                {EXAMPLES[selectedTopic].code}
              </code>
            </pre>
          </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
