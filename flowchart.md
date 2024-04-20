```Mermaid
flowchart TD
    start --> exit[Exit]
    start([Start Menu]) --> use[Use Machine]
    start --> maint[Maintenance]

    maint --> maintMenu[Maintenance Menu]
    maintMenu --> viewStats[View Statistics]
    maintMenu --> resetStats[Reset Statistics]
    maintMenu --> goBackMaint[Go Back]
    goBackMaint --> start

    use --> useMenu[Use Machine Menu]
    useMenu --> insert[Insert Coins]
    useMenu --> selectWash[Select Wash]
    useMenu --> goBackUse[Go Back]
    goBackUse --> start

    insert --> insertMenu[Insert Coins Menu]
    insertMenu --> ins10[Insert 10c]
    insertMenu --> ins20[Insert 20c]
    insertMenu --> ins50[Insert 50c]
    insertMenu --> ins1[Insert $1]
    insertMenu --> goBackIns[Go Back]
    goBackIns --> useMenu

    ins10 --> insertMenu
    ins20 --> insertMenu
    ins50 --> insertMenu
    ins1 --> insertMenu

    selectWash --> washMenu[Select Wash Menu]
    washMenu --> quickWash[Quick Wash]
    washMenu --> mildWash[Mild Wash]
    washMenu --> mediumWash[Medium Wash]
    washMenu --> heavyWash[Heavy Wash]
    washMenu --> goBackWash[Go Back]
    goBackWash --> useMenu

    quickWash --> process{Process Wash}
    mildWash --> process
    mediumWash --> process
    heavyWash --> process

    process --> sufficient{Sufficient Funds?}
    sufficient --> |No| prompt[Prompt Insufficient Funds]
    sufficient --> |Yes| refund[Refund Excess]
    prompt --> washMenu
    refund --> startWash[Start Washing]

    startWash --> lock[Lock Door & Start Wash]
    lock --> progress[Show Progress]
    progress --> completion[Complete Wash]
    completion --> unlock[Unlock Door]
    unlock --> start



    viewStats --> maintMenu
    resetStats --> maintMenu

```
