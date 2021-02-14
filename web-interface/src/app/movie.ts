import { Person } from "./person";
import { Rating } from "./rating";

export interface Movie{
    writers?: Person[]
    directors?: Person[]
    rating?: Rating
    primarytitle?: String
    originaltitle?: String
    titletype?: String
    isadult?: number
    startyear?: number
    endyear?: number
    runtimeminutes?: number
    genres?: String
    imagelink?: String
    description?: String
}