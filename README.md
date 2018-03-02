# Jamnetic Algorhythms
Using Genetic Algorithms to improvise

## Usage
Must use python 3.6
More to come

## Algorithm Thoughts
* GAs for jazz standard - all of me
    * melody only tho, but maintain info about chord progressions
* Mutation = take random note in a measure, maybe for 4 random measures
    * (should we weight based on note length or nah)
    * (or maybe weight based on 'strength' of note position, i.e. notes that fall on beat 1 weighted higher than beats on & of 2)
    * 1. 0.25 probability of picking a random chord tone / note in the key?
        * maybe consider whether or not it's on strong beat
        * add any domain knowledge, or nah?
    * 2a. 0.125 probability of copying a random note already in the measure
    * 2b. 0.125 probability of transposing up/down a whole note
        * 0.5 up, 0.5 down
    * 3a. 0.25 (1 - quanta/4) probability of becoming leading note, chromatic up or down depending on beat?
        * quanta = 1 for quarter note, .5 for eighth, etc.  
    * 3b. 0.25 * (quanta/4) probability of becoming split
        * 0.5 prob of even split
        * 0.25 of triplet
        * 0.25 of dotted and
            * 0.5 of short beat first
            * 0.5 of long beat first
        * apply rules 1,2,4, 7 to new notes
        * apply some min/max, where quanta turns to 0 if it's sixteenth note, also no triplet splitting
    * 4. 0.05 probability of picking note from bar with same chord progression
        * if no such bars exist, we reweight and ignore this possibility
    * 5. 0.05 probability of shifting all notes
        * 0.5 of going to right, 0.5 of going to left
    * 6. 0.05 probability of shuffling notes
        * 0.5 of just shuffling notes themselves
        * 0.5 of shuffling notes + rhythmic structure
    * 7. 0.05 probability of dropping note
    * 8. 0.05 probability of swapping notes
* Crossover ideas
    * split/join
        * Take half of bar and combine to half of other bar
        * probably better to add whole measures
        * alternate every measure?
        * take first half from one and second from other?
* reduce
    * pick pieces w/ highest fitness, leave in some wonky ones, bc "that's jazz"
* fitness function
    * dock points for no note variation
    * dock points for all notes identical to original
    * dock points for having 0 notes from chord progression
    * dock points for only having notes from chord progression
    * dock points for too many jumps
    * dock points if duration is wonky number

Other thoughts
* add inversions to chords
* consider weighting everything based on quanta & 1-quanta
* have a corpus of jazz standards to borrow phrases from