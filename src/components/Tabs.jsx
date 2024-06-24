export default function Tabs({ children, buttons, ButtonsContainer = 'mneu' }) {
    //const ButtonsContainer = buttonsContainer;
    return (
    <>
    <ButtonsContainer>{buttons}</ButtonsContainer>
    {children}
    </>
    )
}